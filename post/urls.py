from django.urls import path
from rest_framework import views
from post.views import *

urlpatterns = [
    path('create/post/', PostCreate.as_view(), name = 'post_create'),
    path('create/image/post/', ImageCreate.as_view(), name = 'image_create'),
    
]