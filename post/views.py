from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from users.models import *
from post.models import *
from post.serializers import *

# Create your views here.

#----------Create Post and Image--------------
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    
    def post(self, request):

        data = self.request.data


        description = data['description']
        location = data['location']

        post = Post.objects.create(
            user_author_code = request.user,
            description = description,
            location = location
        )
        PostSerializer(data=post)
        return Response ({'success': 'post creado con exito'})

class ImageCreate(generics.CreateAPIView):
    serializer_class = ImageSerializer
    
    def post(self, request):

        last_post = Post.objects.filter(user_author_code = request.user.id).last()
        data = self.request.data

        image = data['image']

        new_image= Image.objects.create(
            post_code = last_post,
            image = image
        )
        ImageSerializer(data=new_image)
        return Response ({'success': 'imagen del post guardada con exito'})   




