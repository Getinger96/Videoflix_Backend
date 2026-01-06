from rest_framework import serializers
from django.contrib.auth.models import User


class Registrationserializer(serializers.ModelSerializer):
    confirmed_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','password','confirmed_password']
        extra_kwargs={
            'password':{'write_only':True},
            'email':{'required':True}
        }

        def validate_email(self,value):
            if User.objects.filter(email=value).exists():
             raise serializers.ValidationError('Email already exists')
            return value