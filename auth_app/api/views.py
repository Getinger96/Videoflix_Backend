from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import Registrationserializer,CustomTokenObtainPairSerializer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

User = get_user_model()

class RegistrationView(CreateAPIView):
    serializer_class = Registrationserializer
    
    def post(self, request):
        # Handle user registration logic here

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            site=request.get_host()
            print(site)
            mail_subject='Confirmation message'
            token=account_activation_token.make_token(user)
            message=render_to_string('acc_active_email.html',{
                'user':user,
                'domain':site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token,
            })
            to_email=serializer.validated_data.get('email')
            to_list=[to_email]
            from_email='erich.getinger@outlook.de'
            send_mail(mail_subject,message,from_email,to_list,fail_silently=False)
            registration_response={
                'user':{
                    'id':user.id,
                    'email':user.email,
                },
                'token':token
            }
            return Response(registration_response, status=201)
        else:
            return Response(serializer.errors, status=400)    
        
        


class ActivationView(APIView):
    def get(self, request, uidb64, token):
        # Handle account activation logic here
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully'}, status=200)
        


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        data={
            'id':serializer.user.id,
            'username':serializer.user.username,


        }
        refresh = serializer.validated_data["refresh"]
        access= serializer.validated_data["access"]
        response =Response({"detail":"Login erfolgreich",'user':data},status=status.HTTP_200_OK)

        response.set_cookie(
            key= "access_token",
            value= access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key= "refresh_token",
            value= refresh,
            httponly=True,
            secure=True,
            samesite="Lax"

        )
        
        return response 
    

class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token=request.COOKIES.get("refresh_token")
        if refresh_token is None:
            return Response({"detail":"Refresh token not found!"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer=self.get_serializer(data={"refresh":refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({"detail":"Refresh token invalid!"},
                            status=status.HTTP_401_UNAUTHORIZED)
        access_token=serializer.validated_data.get("access")
        response=Response({"message":"access token refreshed"})
        response.set_cookie(
            key= "access_token",
            value= access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        return response
    


class LogoutView(APIView):
     """
    API view for logging out a user.
    Deletes the refresh token by blacklisting it and
    removes the cookie from the client.
    """
     permission_classes=[IsAuthenticated]
     def post(self,request):
        refresh_token=request.COOKIES.get("refresh_token")
        refresh_token=RefreshToken(refresh_token)
        refresh_token.blacklist()
        response=Response()
        response.delete_cookie("refresh_token")
        response.data={"detail":"Logout successfully! All Tokens will be deleted. Refresh token is now invalid"}
        return response