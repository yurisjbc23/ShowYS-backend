from distutils.log import error
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics, status

from .serializers import RegisterSerializer, LoginSerializer
from .permissions import IsUserActivate
from post.models import Post
from .models import Profile

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
        
class LoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
                posts = Post.objects.filter(user = user.id)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': user,
                    'post': [post for post in posts],
                },200)
            except Exception as e:
                return Response({'error': str(e)}, 500)
        else:
            return Response(serializer.errors, 400)
        
class LogoutView(APIView):
    permission_classes = (IsUserActivate,)
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
