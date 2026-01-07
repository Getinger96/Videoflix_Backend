from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import Registrationserializer
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

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
            mail_subject='Confirmation message'
            message=render_to_string('acc_active_email.html',{
                'user':user,
                'domain':site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email=serializer.validated_data.get('email')
            to_list=[to_email]
            from_email='noreply@{site}.com'
            send_mail(mail_subject,message,from_email,to_list,fail_silently=True)
            return Response(serializer.data, status=201)
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