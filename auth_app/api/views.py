from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import Registrationserializer,CustomTokenObtainPairSerializer,PasswortResetSerializer, PasswortConfirmSerializer
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
    """
    Mixin to provide additional context data for password-related views.
    """

    extra_context = None

    def get_context_data(self, **kwargs):
        """
        Extend the default context with title, subtitle, and extra context.

        :return: Updated context dictionary
        """
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context


class RegistrationView(CreateAPIView):
    """
    API view for user registration.

    Creates a new inactive user account and sends
    an email with an activation link.
    """

    serializer_class = Registrationserializer

    def post(self, request):
        """
        Handle user registration.

        - Validate input data
        - Create inactive user
        - Generate activation token
        - Send activation email

        :param request: HTTP request with registration data
        :return: Response with user info or validation errors
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            site = request.get_host()
            mail_subject = 'Confirmation message'
            token = account_activation_token.make_token(user)

            message = render_to_string(
                'acc_active_email.html',
                {
                    'user': user,
                    'domain': site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                }
            )

            to_email = serializer.validated_data.get('email')
            send_mail(
                mail_subject,
                message,
                'erich.getinger@outlook.de',
                [to_email],
                fail_silently=False
            )

            return Response(
                {
                    'user': {
                        'id': user.id,
                        'email': user.email,
                    },
                    'token': token
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    """
    API view for activating a user account via email link.
    """

    def get(self, request, uidb64, token):
        """
        Activate the user account if the token is valid.

        :param uidb64: Base64 encoded user ID
        :param token: Activation token
        :return: Activation status message
        """
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {'message': 'Account activated successfully'},
                status=status.HTTP_200_OK
            )


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that stores JWT tokens in HttpOnly cookies.
    """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user and set access/refresh tokens as cookies.

        :return: Response with user info and cookies
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        response = Response(
            {
                "detail": "Login successful",
                "user": {
                    "id": serializer.user.id,
                    "username": serializer.user.username,
                }
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response


class CookieRefreshView(TokenRefreshView):
    """
    API view for refreshing the access token using cookies.
    """

    def post(self, request, *args, **kwargs):
        """
        Refresh the access token using the refresh token stored in cookies.

        :return: New access token in HttpOnly cookie
        """
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not found!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"detail": "Refresh token invalid!"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = serializer.validated_data.get("access")

        response = Response({"message": "Access token refreshed"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response


class LogoutView(APIView):
    """
    API view for logging out a user.

    Blacklists the refresh token and removes it from cookies.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Invalidate the refresh token and log the user out.

        :return: Logout confirmation message
        """
        refresh_token = request.COOKIES.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response(
            {
                "detail": (
                    "Logout successful. Refresh token is invalidated "
                    "and all tokens are removed."
                )
            }
        )
        response.delete_cookie("refresh_token")
        return response


class PasswortResetView(CreateAPIView):
    """
    API view for requesting a password reset via email.
    """

    serializer_class = PasswortResetSerializer

    def post(self, request):
        """
        Send a password reset email with a secure token.

        :return: Confirmation message
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data.get('email'))
            site = request.get_host()
            token = account_activation_token.make_token(user)

            message = render_to_string(
                'password_reset_subject.html',
                {
                    'user': user,
                    'domain': site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                }
            )

            send_mail(
                'Password Reset',
                message,
                'erich.getinger@outlook.de',
                [user.email],
                fail_silently=False
            )

            return Response(
                {'detail': 'An email has been sent to reset your password'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswortResetConfirmView(APIView):
    """
    API view for confirming and setting a new password.
    """

    serializer_class = PasswortConfirmSerializer

    def post(self, request, uidb64, token):
        """
        Validate the reset token and update the user's password.

        :param uidb64: Base64 encoded user ID
        :param token: Password reset token
        :return: Password reset status
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {'message': 'Password has been reset successfully'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Invalid link or token'},
            status=status.HTTP_400_BAD_REQUEST
        )