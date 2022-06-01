from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

import re

from .models import Profile


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
    date_birth = serializers.DateField(required=True)
    phone = serializers.CharField(required=True, max_length=20)

    class Meta:
        # https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name',
                  'date_birth', 'phone')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                "Password fields didn't match.", code='password')
        if not attrs['first_name'] or not attrs['last_name']:
            raise serializers.ValidationError(
                'You must provide a first or last name.', code='first_name')
        return attrs


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        if username and password:
            user = None
            regex_email = re.compile(
                r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            regex_username = re.compile(
                r'^[a-zA-Z0-9_][a-zA-Z0-9_.]*')
            if re.fullmatch(regex_email, username) or re.fullmatch(regex_username, username):
                if re.fullmatch(regex_email, username):
                    user = authenticate(request=self.context.get('request'),
                                        email=username, password=password)
                else:
                    user = authenticate(request=self.context.get('request'),
                                        username=username, password=password)
            else:
                raise serializers.ValidationError(
                    'The format is invalid for both an email and a username', code='authorization')
            if not user:
                raise serializers.ValidationError(
                    'Access denied: wrong username or password.', code='authorization')
        else:
            raise serializers.ValidationError(
                'Both "username" and "password" are required.', code='authorization')
        attrs['user'] = user
        return attrs
