from distutils.log import error
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
                return Response({}, 200)
            except Exception as e:
                return Response({'error':str(e)}, 500)
        else:
            return Response(serializer.errors, 400)