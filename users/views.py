from distutils.log import error
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
    # permission_classes = (AllowAny,)
    # def get(self, request, format=None):
    #     user = request.user
    #     followers = [f.user_from for f in Follow.objects.filter(user_to=user.id)]
    #     posts = [post for post in Post.objects.filter(pk__in=followers).order_by()]
    # queryset=User.objects.all()
    serializer_class = UserSerializer 

    # def get_queryset(self):
    #     queryset=User.objects.filter(id=8)
    #     return queryset
    def get(self, request, format=None):
        user = request.user
        followers = [f.user_to.id for f in Follow.objects.filter(user_from=user.id)]
        # followers = [f.user_to for f in Follow.objects.filter(user_from=8)]
        feed = [post for post in Post.objects.filter(user_author_code__in=followers).order_by('created_date')]
        home = HomeSerializer(feed, many=True)
        return Response(home.data)