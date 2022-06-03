from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

import re

from .models import Profile
from post.serializers import *

class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=10)

class CreateProfileSerializer(serializers.Serializer):
    date_birth = serializers.DateField()
    phone = serializers.CharField(max_length=20)

class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    photo = serializers.ImageField(max_length=255)
    biography = serializers.CharField(max_length=255, allow_blank=True)
    post = serializers.IntegerField()
    followers = serializers.IntegerField()
    following = serializers.IntegerField()

class GetUpdateUserProfileSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    photo = serializers.ImageField(max_length=255)
    biography = serializers.CharField(max_length=255, allow_blank=True,  allow_null=True)
    date_birth = serializers.DateField()
    phone = serializers.CharField(max_length=20)
    is_private = serializers.BooleanField()


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

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    follow = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', 'id','image','follow')
    def get_image(self, user):
        profile = Profile.objects.get(user=user.id)
        return ImageSerializer(profile, many=False).data['photo']
    def get_follow(self, user):
        current_user = self.context.get('user_id')
        follow_data = bool(Follow.objects.filter(user_from=current_user,user_to=user.id).count())
        return follow_data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['photo']

class HomeSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    def get_user(self, post):
        current_user = self.context.get('user_id')
        user_data = User.objects.get(id=post.user_author_code.id)
        return UserSerializer(user_data, many=False, context ={'user_id': current_user}).data
    def get_post(self, post):
        current_user = self.context.get('user_id')
        return PostSerializer(post, many=False, context ={'user_id': current_user}).data
    
# class HomeSerializer(serializers.ModelSerializer):
#     id = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     class Meta:
#         model = Image
#         fields = ['image']
        
#     def get_id(self, post):
#         return post.code
        
#     def get_image(self, post):
        
#         return PostSerializer(post, many=False, context ={'user_id': current_user}).data
