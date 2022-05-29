from django.urls import path
from rest_framework import views
from post.views import *

urlpatterns = [
    path('create/post/', PostCreate.as_view(), name = 'post_create'),
    path('create/image/post/', ImageCreate.as_view(), name = 'image_create'),
    path('create/comment/post/<int:pk>/', CommentCreate.as_view(), name = 'comment_create'),
    path('delete/comment/<int:pk>/', CommentDelete.as_view(), name = 'comment_delete'),
    path('create/delete/favorite/post/<int:pk>/', FavoriteCreateDelete.as_view(), name = 'favorite_create_delete'),
    
]