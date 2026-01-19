from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class Registrationserializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','confirmed_password']
        extra_kwargs={
            'password':{'write_only':True},
            'email':{'required':True}
            
        }

    def validate_confirmed_password(self, value):
         """
        Ensure that the confirmed password matches the original password.
        If not, raise a validation error.
        """
         password = self.initial_data.get('password')
         if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
         return value


    def validate_email(self,value):
            if User.objects.filter(email=value).exists():
             raise serializers.ValidationError('Email already exists')
            return value
        

    def save(self):
         """
         Create and save a new user instance.
         The password is hashed using Django's built-in set_password method.
         """
         
         pw = self.validated_data['password']
         account = User(email=self.validated_data['email'], username=self.validated_data['username'])
         account.set_password(pw)
         account.save()
         return account
        


User=get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop("username")

    def validate(self,attrs):
        email=attrs.get("email")
        password=attrs.get("password")
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
         raise serializers.ValidationError("ungültige Email oder Password")
        if not user.check_password(password):
            raise serializers.ValidationError("ungültige Email oder Password")
        attrs['username']=user.username
        data=super().validate(attrs)
        return data
    

class PasswortResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")
        return value
    

class PasswortConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirmed_password = data.get('confirmed_password')
        if new_password != confirmed_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data