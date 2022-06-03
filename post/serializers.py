from rest_framework import serializers
from post.models import *
from users.models import *
    
class PostSerializer(serializers.ModelSerializer):
    likesCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('code', 'description','likesCount','commentsCount','image','created_date','favorite')
    def get_likesCount(self, post):
        like = Like.objects.filter(post_code=post.code, user_author_code=post.user_author_code.id).count()
        return like
    def get_commentsCount(self, post):
        comment = Comment.objects.filter(post_code=post.code, user_author_code=post.user_author_code.id).count()
        return comment    
    def get_image(self, post):
        image = [img.image for img in Image.objects.filter(post_code=post.code)]
        return ImagePostSerializer({'image':image}, many=False).data['image']
    def get_favorite(self, post):
        current_user = self.context.get('user_id')
        favorite_data = bool(Favorite.objects.filter(post_code=post.code, user_author_code=current_user).count())
        return favorite_data

        
class ImagePostSerializer(serializers.Serializer):
    image = serializers.ListField(child = serializers.ImageField(max_length=255))

class PostCreateSerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child = serializers.CharField(max_length=50, required=True))
    images = serializers.ListField(child = serializers.ImageField(max_length=255, required=True))
    class Meta:
        model = Post
        fields = ['description','location','hashtags','images']
    def validate(self, attrs):
        if len(attrs['hashtags']) == 0:
            raise serializers.ValidationError(
                "You must provide 1 or more hashtag.", code='hashtags')
        if len(attrs['images']) == 0:
            raise serializers.ValidationError(
                'You must provide 1 or more images.', code='images')
        return attrs

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