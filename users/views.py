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