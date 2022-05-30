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