from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from users.models import *
from users.serializers import *
from post.models import *

# Create your views here.

#-------Create User and Profile (Signup)---------
"no encripta las contraseñas"

class CreateUser(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    def post(self, request):

        data = self.request.data

        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']
        
        
        """Validamos que el usuario no exista"""
        if User.objects.filter(username=username).exists():
            return Response({ 'error': 'El username ya existe' })
        elif User.objects.filter(email=email).exists():
            return Response({ 'error': 'El correo ya existe' })
        elif len(password) < 10:
            return Response({ 'error': 'La contraseña debe maximo 9 caracteres' })
        else:
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password
            )
                    
            CreateUserSerializer(data=user)
            return Response ({'success': 'usuario creado con exito'})

class CreateProfile(generics.CreateAPIView):
    serializer_class = CreateProfileSerializer
    def post(self, request):
        user = User.objects.latest('date_joined')
        #user = User.objects.filter(id = pk)
        #user = User.objects.get(id=request.user.id)

        data = self.request.data

        date_birth = data['date_birth']
        phone = data['phone']

        profile = Profile.objects.create(
            user=user,
            date_birth = date_birth,
            phone = phone
        )
        
        CreateProfileSerializer(data=profile)
        return Response ({'success': 'cuenta de usuario creada con exito'})

#--------Follow User and Unfollow User---------------
class FollowUnfollow(generics.DestroyAPIView):
    def delete(self, request, pk):
        other_user = User.objects.filter(id = pk).first()

        if Follow.objects.filter(user_from = request.user.id, user_to = other_user.id).exists():
            
            unfollow = Follow.objects.filter(user_from = request.user.id, user_to = other_user.id).first()
            unfollow.delete()
            return Response ({'success': 'unfollow exitoso'})
        else:
            Follow.objects.create(
                user_from = request.user,
                user_to = other_user
            )
            return Response ({'success': 'follow exitoso'})

#---------------------Retrieve my profile------------------------------------
"falta traer la lista de imagenes"
class MyProfileRetrieve(generics.RetrieveAPIView):

    def get(self, request):
        user = request.user
        profile = request.user.profile
        user_post = Post.objects.filter(user_author_code = user.id)

        data_user_profile = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'username' : user.username,
            'photo' : profile.photo,
            'bio' : profile.biography,
            'post' : user_post.count(),
            'followers' : Follow.objects.filter(user_to = user.id).count(),
            'following' : Follow.objects.filter(user_from = user.id).count()
            }
        user_profile_serializer = UserProfileSerializer(data = data_user_profile)
        if user_profile_serializer.is_valid():
            return Response(user_profile_serializer.data, status = status.HTTP_200_OK)

#-----------------Retrieve other user profile--------------------------------
"falta traer la lista de imagenes"
class OtherProfileRetrieve(generics.RetrieveAPIView):

    def get(self, request, pk):
        user = User.objects.filter(id = pk)
        profile = user.profile
        user_post = Post.objects.filter(user_author_code = user.id)

        if profile.is_private == True:

            if Follow.objects.filter(user_from = request.user.id, user_to = user.id).exists():
                #debe traer las imagenes
                
                data_user_profile = {
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'photo' : profile.photo,
                'bio' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
                user_profile_serializer = UserProfileSerializer(data = data_user_profile)
                if user_profile_serializer.is_valid():
                    return Response(user_profile_serializer.data, status = status.HTTP_200_OK)

            else:# aqui NO debe traer imagenes
                data_user_profile = {
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'photo' : profile.photo,
                'bio' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
                user_profile_serializer = UserProfileSerializer(data = data_user_profile)
                if user_profile_serializer.is_valid():
                    return Response(user_profile_serializer.data, status = status.HTTP_200_OK)

        else:#aqui si debe traer las imagenes

            data_user_profile = {
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'photo' : profile.photo,
                'bio' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
            user_profile_serializer = UserProfileSerializer(data = data_user_profile)
            if user_profile_serializer.is_valid():
                return Response(user_profile_serializer.data, status = status.HTTP_200_OK)