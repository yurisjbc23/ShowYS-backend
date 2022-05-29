from rest_framework import serializers
from post.models import *

class PostSerializer(serializers.Serializer):
    
    description = serializers.CharField(max_length=1000)
    location = serializers.CharField(max_length=50)

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['image']