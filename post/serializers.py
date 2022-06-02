from rest_framework import serializers
from post.models import *
from users.models import *
    
class PostSerializer(serializers.ModelSerializer):
    likesCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('code', 'description','likesCount','commentsCount','image','created_date')
    def get_likesCount(self, post):
        like = Like.objects.filter(post_code=post.code, user_author_code=post.user_author_code.id).count()
        return like
    def get_commentsCount(self, post):
        comment = Comment.objects.filter(post_code=post.code, user_author_code=post.user_author_code.id).count()
        return comment    
    def get_image(self, post):
        image = [img.image for img in Image.objects.filter(post_code=post.code)]
        return ImagePostSerializer({'image':image}, many=False).data['image']
        
class ImagePostSerializer(serializers.Serializer):
    image = serializers.ListField(child = serializers.ImageField(max_length=255))

class PostSerializer2(serializers.Serializer):
    
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