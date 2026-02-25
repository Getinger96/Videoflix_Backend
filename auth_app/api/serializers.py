from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import  TokenObtainPairSerializer
User = get_user_model()

class Registrationserializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles creation of a new user account, including:
    - Username
    - Email
    - Password confirmation
    """ 

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta configuration for Registrationserializer.
        """
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_confirmed_password(self, value):
        """
        Ensure that the confirmed password matches the original password.

        :param value: The confirmed password provided by the user
        :return: The validated confirmed password
        :raises ValidationError: If passwords do not match
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        """
        Validate that the email address is unique.

        :param value: Email address provided by the user
        :return: The validated email
        :raises ValidationError: If the email already exists
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Create and save a new user instance.

        The password is securely hashed using Django's set_password method.

        :return: The created User instance
        """
        pw = self.validated_data['password']
        username = self.validated_data['email'].split('@')[0]
        if User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count() + 1}"
        account = User(
            email=self.validated_data['email'],
            username=username
        )
        account.set_password(pw)
        account.save()
        return account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extended JWT serializer that embeds additional user information
    into the token response.
    """

    username_field = User.USERNAME_FIELD  
    """Defines the field used as the username identifier (e.g. 'email' or 'username')."""

    def validate(self, attrs):
        """
        Validates the login credentials and extends the JWT response.

        Args:
            attrs (dict): The incoming authentication data (e.g. username & password).

        Returns:
            dict: The token response, extended with the user's 'email' and 'id'.
        """
        data = super().validate(attrs)  
        """Calls the parent class – verifies credentials and generates access & refresh tokens."""
        
        data['email'] = self.user.email  
        """Adds the authenticated user's email address to the response."""
        
        data['id'] = self.user.id
        """Adds the authenticated user's ID to the response."""
        
        return data

    
class PasswortResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset via email.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Ensure a user exists for the given email address.

        :param value: Email address
        :return: The validated email
        :raises ValidationError: If no user is found
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user is associated with this email address."
            )
        return value


class PasswortConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming and setting a new password.
    """

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure that the new password and confirmation match.

        :param data: Dictionary containing both passwords
        :return: Validated data
        :raises ValidationError: If passwords do not match
        """
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data