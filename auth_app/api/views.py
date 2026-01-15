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
from django.contrib.auth.decorators import login_not_required, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

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
     


class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
         """
        Handle POST request to invalidate the refresh token.
        Removes refresh_token cookie and blacklists the token.
        """
         refresh_token=request.COOKIES.get("refresh_token")
         """
        Convert the token into a RefreshToken object.
        This allows the token to be blacklisted.
        """
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
         response=Response({"detail":" Token refreshed",'access':access_token})
         """
        Save the new access token as an HttpOnly cookie.
        This cookie replaces the old access token.
        """
         response.set_cookie(
            key= "access_token",
            value= access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
         return response
    

@method_decorator(login_not_required, name="dispatch")
class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "templates/password_reset_subject.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "templates/password_reset_subject.html"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"