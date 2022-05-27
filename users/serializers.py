from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import re

class RegisterSerializer(serializers.ModelSerializer):
    # https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5
    # We can create new atributes for changing model validations.
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.RegexField(
        "^[a-zA-Z0-9_][a-zA-Z0-9_.]*",
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # https://www.django-rest-framework.org/api-guide/fields/#write_only
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
        model = User
        
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):   
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})            
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
