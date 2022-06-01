from rest_framework import serializers
from users.models import *
from post.models import *

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
    bio = serializers.CharField(max_length=255)
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