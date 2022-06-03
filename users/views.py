from distutils.log import error
from urllib import response
from django.contrib.auth.models import User

from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import viewsets

from .serializers import *
from .permissions import IsUserActivate
from post.models import Post
from .models import Profile, Follow

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
            'biography' : profile.biography if profile.biography else '',
            'post' : user_post.count(),
            'followers' : Follow.objects.filter(user_to = user.id).count(),
            'following' : Follow.objects.filter(user_from = user.id).count()
            }
        user_profile_serializer = UserProfileSerializer(data = data_user_profile)
        if user_profile_serializer.is_valid():
            return Response(user_profile_serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(user_profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

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
                'biography' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
                user_profile_serializer = UserProfileSerializer(data = data_user_profile)
                if user_profile_serializer.is_valid():
                    return Response(user_profile_serializer.data, status = status.HTTP_200_OK)
                else:
                    return Response(user_profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

            else:# aqui NO debe traer imagenes
                data_user_profile = {
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'photo' : profile.photo,
                'biography' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
                user_profile_serializer = UserProfileSerializer(data = data_user_profile)
                if user_profile_serializer.is_valid():
                    return Response(user_profile_serializer.data, status = status.HTTP_200_OK)
                else:
                    return Response(user_profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        else:#aqui si debe traer las imagenes

            data_user_profile = {
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'username' : user.username,
                'photo' : profile.photo,
                'biography' : profile.biography,
                'post' : user_post.count(),
                'followers' : Follow.objects.filter(user_to = user.id).count(),
                'following' : Follow.objects.filter(user_from = user.id).count()
                }
            user_profile_serializer = UserProfileSerializer(data = data_user_profile)
            if user_profile_serializer.is_valid():
                return Response(user_profile_serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(user_profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#--------------Retrieve and Update my user profile--------------
class MyProfileUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = GetUpdateUserProfileSerializer
   
    def get(self, request):
        user = request.user
        profile = request.user.profile
        user_post = Post.objects.filter(user_author_code = user.id)


        data_profile = {
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'username' : user.username,
            'photo' : profile.photo,
            'biography' : profile.biography,
            'date_birth': profile.date_birth,
            'phone': profile.phone,
            'numberPosts' : user_post.count(),
            'followers' : Follow.objects.filter(user_to = user.id).count(),
            'following' : Follow.objects.filter(user_from = user.id).count(),
            'is_private' : profile.is_private
        }

        profile_serializer = GetUpdateUserProfileSerializer(data = data_profile)
        if profile_serializer.is_valid():
            return Response(profile_serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

    def put(self, request):
        user = request.user
    
        data_profile = self.request.data

        first_name = data_profile['first_name']
        last_name = data_profile['last_name']
        username =data_profile['username']
        date_birth = data_profile['date_birth']
        phone = data_profile['phone']
        biography = data_profile['biography']
        photo = data_profile['photo']
        is_private = data_profile['is_private']

        User.objects.filter(id = user.id).update(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
            
        Profile.objects.filter(user = user.id).update(
            date_birth = date_birth, 
            phone = phone, 
            biography = biography, 
            photo = photo, 
            is_private = is_private
        )
        return Response({'message': 'perfil de usuario modificado con exito'}, status = status.HTTP_200_OK)
      
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = User.objects.create(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name']
                )
                user.set_password(serializer.validated_data['password'])
                user.save()
                profile = Profile.objects.create(
                    user=user,
                    date_birth=serializer.validated_data['date_birth'],
                    phone=serializer.validated_data['phone'],
                )
                profile.save()
                return Response({'successful':'The user was successfully registered'}, 200)
            except Exception as e:
                return Response({'error': str(e)}, 500)
        else:
            return Response(serializer.errors, 400)
        
class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
                posts = Post.objects.filter(user_author_code = user.id)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                             },
                    'post': [post for post in posts],
                },200)
            except Exception as e:
                return Response({'error': str(e)}, 500)
        else:
            return Response(serializer.errors, 400)
        
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                posts = Post.objects.filter(user_author_code = user.id)
                return Response({
                    'isAuthenticated': 'successfully',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                             },
                    'post': [post for post in posts],
                },200)
            else:
                return Response({'isAuthenticated': 'error'}, 400)
        except:
                return Response({'isAuthenticated': 'error'}, 500)
        
class LogoutView(APIView):
    permission_classes = (IsUserActivate,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class HomeView(APIView):
    serializer_class = HomeSerializer 
    def get(self, request, format=None):
        try:
            user = request.user
            followers = [f.user_to.id for f in Follow.objects.filter(user_from=user.id)]
            feed = [post for post in Post.objects.filter(user_author_code__in=followers).order_by('created_date')]
            home = HomeSerializer(feed, many=True, context ={'user_id': request.user.id})
            return Response(home.data)
        except Exception as e:
            return Response({'response':str(e)},500)

