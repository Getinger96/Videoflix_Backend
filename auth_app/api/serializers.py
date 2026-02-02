from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        fields = ['username', 'email', 'password', 'confirmed_password']
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
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        account.set_password(pw)
        account.save()
        return account


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that authenticates users via email instead of username.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """
        Remove the default username field from the serializer.
        """
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            self.fields.pop("username")

    def validate(self, attrs):
        """
        Validate user credentials using email and password.

        :param attrs: Dictionary containing email and password
        :return: JWT token data
        :raises ValidationError: If credentials are invalid
        """
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        attrs['username'] = user.username
        data = super().validate(attrs)
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
    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure that the new password and confirmation match.

        :param data: Dictionary containing both passwords
        :return: Validated data
        :raises ValidationError: If passwords do not match
        """
        new_password = data.get('new_password')
        confirmed_password = data.get('confirmed_password')

        if new_password != confirmed_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data