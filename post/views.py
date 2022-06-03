from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

import datetime
from django.utils import timezone

from users.models import *
from users.serializers import *
from post.models import *
from post.serializers import *
from .utils import checkFriendship
# Create your views here.

#----------Create Post and Image--------------
class PostCreate(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                post = Post.objects.create(
                    user_author_code=request.user.id,
                    description=serializer.validated_data['description'],
                    location=serializer.validated_data['location'],
                )
                post.save()
                for img in serializer.validated_data['images']:
                    image = Image.objects.create(
                        post_code=post.code,
                        image=img,
                    )
                    image.save()
                for h in serializer.validated_data['hashtags']:
                    exist = Hashtag.objects.filter(name=h).first()
                    if not exist:
                        hashtag = Hashtag.objects.create(
                            name=h,
                        )
                        hashtag.save()
                        postHashtag = PostHashtag.objects.create(
                            post_code=post.code,
                            hashtag_code=hashtag.code
                        )
                        postHashtag.save()
                    else:
                        postHashtag = PostHashtag.objects.create(
                            post_code=post.code,
                            hashtag_code=exist.code
                        )
                        postHashtag.save()
                return Response({'successful':'The post was successfully published'}, 200)
            except Exception as e:
                return Response({'error': str(e)}, 500)
        else:
            return Response(serializer.errors, 400)


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

#------------------Delete Post--------------------------
class PostDelete(generics.DestroyAPIView):
    def delete(self, request, pk):

        if Post.objects.filter(code = pk, user_author_code = request.user.id).exists():

            post = Post.objects.filter(code = pk, user_author_code = request.user.id).first()
            now = timezone.now()
            twenty_four_hours_ago = post.created_date + datetime.timedelta(hours=24)

            if now < twenty_four_hours_ago:

                post.delete()
                return Response ({'success': 'post eliminado con exito'})

            else:
                return Response ({'message': 'el post no puede ser eliminado han pasado mas de 24 horas desde su creacion'})
    
        else:
            return Response ({'error': 'el post no existe'})

class FavoriteGalleryView(APIView):
    serializer_class = GalerySerializer 
    def get(self, request, format=None):
        try:
            user = request.user
            code_list = [post.user_author_code for post in Favorite.objects.filter(user_author_code=user.id).order_by('created_date')]
            favorite_posts = [post for post in Post.objects.filter(code__in=code_list)]
            favorite = GalerySerializer(favorite_posts, many=True, context ={'user_id': user.id})
            return Response(favorite.data)
        except Exception as e:
            return Response({'response':str(e)},500)

class FavoriteView(APIView):
    serializer_class = HomeSerializer 
    def get(self, request, format=None):
        try:
            user = request.user
            code_list = [post.user_author_code for post in Favorite.objects.filter(user_author_code=user.id).order_by('created_date')]
            favorite_posts = [post for post in Post.objects.filter(code__in=code_list)]
            favorite = HomeSerializer(favorite_posts, many=True, context ={'user_id': user.id})
            return Response(favorite.data)
        except Exception as e:
            return Response({'response':str(e)},500)

class ProfilePostGaleryView(APIView):
    serializer_class = GalerySerializer 
    def get(self, request, pk , format=None):
        try:
            user = User.objects.filter(id=pk).first()
            if user:
                if (user.is_private and checkFriendship(request.user.id,user.id)) or (not user.is_private):
                    profile_posts = [post for post in Post.objects.filter(user_author_code=user.id)]
                    posts = GalerySerializer(profile_posts, many=True, context ={'user_id': user.id})
                    return Response(posts.data)
                else:
                    return Response({'response':"private"},200)
            else:
                return Response({'response':"That user doesn't exist"},400)
        except Exception as e:
            return Response({'response':str(e)},500)  
        
class ProfilePostExploreView(APIView):
    serializer_class = HomeSerializer 
    def get(self, request, pk , format=None):
        try:
            user = User.objects.filter(id=pk).first()
            if user:
                if (user.is_private and checkFriendship(request.user.id,user.id)) or (not user.is_private):
                    profile_posts = [post for post in Post.objects.filter(user_author_code=user.id)]
                    posts = HomeSerializer(profile_posts, many=True, context ={'user_id': user.id})
                    return Response(posts.data)
                else:
                    return Response({'response':"private"},200)
            else:
                return Response({'response':"That user doesn't exist"},400)
        except Exception as e:
            return Response({'response':str(e)},500)        

class CurrentProfilePostGalleryView(APIView):
    serializer_class = GalerySerializer 
    def get(self, request, format=None):
        try:
            user = request.user
            profile_posts = [post for post in Post.objects.filter(user_author_code=user.id)]
            posts = GalerySerializer(profile_posts, many=True, context ={'user_id': user.id})
            return Response(posts.data)
        except Exception as e:
            return Response({'response':str(e)},500)

class CurrentProfilePostExploreView(APIView):
    serializer_class = HomeSerializer 
    def get(self, request, format=None):
        try:
            user = request.user
            profile_posts = [post for post in Post.objects.filter(user_author_code=user.id)]
            posts = HomeSerializer(profile_posts, many=True, context ={'user_id': user.id})
            return Response(posts.data)
        except Exception as e:
            return Response({'response':str(e)},500)