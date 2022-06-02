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

    serializer_class = PostSerializer2
    
    def post(self, request):

        data = self.request.data


        description = data['description']
        location = data['location']

        post = Post.objects.create(
            user_author_code = request.user,
            description = description,
            location = location
        )

        PostSerializer2(data=post)
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

#----------------Create and Delete hashtag Post-------------
class HashtagCreate(generics.CreateAPIView):
    serializer_class = HashtagSerializer

class PostHashtagCreateDelete(generics.DestroyAPIView):
    def delete(self, request, pk):

        last_post = Post.objects.filter(user_author_code = request.user.id).latest('created_date')

        if Hashtag.objects.filter(code = pk).exists():
            hashtag = Hashtag.objects.filter(code = pk).first()
            if PostHashtag.objects.filter(post_code = last_post.code, hashtag_code = hashtag.code).exists():
               post_hashtag = PostHashtag.objects.filter(post_code = last_post.code, hashtag_code = hashtag.code).first()
               post_hashtag.delete()
               return Response ({'success': 'hashtag eliminado del post de forma exitosa'})
            else:
                PostHashtag.objects.create(
                    post_code = last_post,
                    hashtag_code = hashtag
                )
                return Response ({'message': 'el hashtag ha sido agregado con exito al post'})
        else:
            return Response ({'error': 'el hashtag no existe'})  

#----------------Create comment----------------------
class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def post(self, request, pk):
        post = Post.objects.filter(code = pk).first()
        data = self.request.data

        message = data['message']
        
        comment = Comment.objects.create(
            user_author_code = request.user,
            post_code = post,
            message = message
        )

        CommentSerializer(data=comment)
        return Response ({'success': 'comentario creado con exito'})

#----------------Delete comment----------------------------
class CommentDelete(generics.DestroyAPIView):

    def delete(self, request, pk):
        comment=Comment.objects.filter(code = pk).first()
        comment.delete()
        return Response ({'success': 'comentario eliminado con exito'})

#--------add Post to Favorite and Delete Post from Favorite------
class FavoriteCreateDelete(generics.DestroyAPIView):

    def delete(self, request, pk):
        post = Post.objects.filter(code = pk).first()

        if Favorite.objects.filter(post_code = post.code).exists():
            
            post_favorite=Favorite.objects.filter(post_code = post.code).first()
            post_favorite.delete()
            return Response ({'success': 'post eliminado de fovoritos con exito'})
        else:
            Favorite.objects.create(
                user_author_code = request.user,
                post_code = post
            )
            return Response ({'success': 'favorito creado con exito'})

#------------Create Like and Delete Like------
class LikeCreateDelete(generics.DestroyAPIView):

    def delete(self, request, pk):
        post = Post.objects.filter(code = pk).first()

        if Like.objects.filter(post_code = post.code).exists():
            
            post_like=Like.objects.filter(post_code = post.code).first()
            post_like.delete()
            return Response ({'success': 'like eliminado del post con exito'})
        else:
            Like.objects.create(
                user_author_code = request.user,
                post_code = post
            )

            return Response ({'success': 'like en post agregado con exito'})
