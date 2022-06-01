from rest_framework import serializers
from post.models import *

class PostSerializer(serializers.Serializer):
    
    description = serializers.CharField(max_length=1000)
    location = serializers.CharField(max_length=50)

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['image']

class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = '__all__'

class CommentSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)