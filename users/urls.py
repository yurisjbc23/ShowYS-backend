from django.urls import path
from rest_framework import views
from users.views import *

urlpatterns = [
    path('create/user/', CreateUser.as_view(), name = 'user_create'),
    path('create/profile/', CreateProfile.as_view(), name = 'profile_create'),
    
]