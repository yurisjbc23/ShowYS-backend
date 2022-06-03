from django.urls import path
from rest_framework import views
from post.views import *

urlpatterns = [
    path('create/post/', PostCreate.as_view(), name = 'post_create'),
    path('create/image/post/', ImageCreate.as_view(), name = 'image_create'),
    path('create/hashtag/', HashtagCreate.as_view(), name = 'hashtag_create'),
    path('create/post/hashtag/<int:pk>/', PostHashtagCreateDelete.as_view(), name = 'post_hashtag_create_delete'),
    path('create/comment/post/<int:pk>/', CommentCreate.as_view(), name = 'comment_create'),
    path('delete/comment/<int:pk>/', CommentDelete.as_view(), name = 'comment_delete'),
    path('create/delete/favorite/post/<int:pk>/', FavoriteCreateDelete.as_view(), name = 'favorite_create_delete'),
    path('create/delete/like/post/<int:pk>/', LikeCreateDelete.as_view(), name = 'like_create_delete'),
    path('delete/post/<int:pk>/', PostDelete.as_view(), name = 'post_delete'),
    
    path('gallery/favorite/', FavoriteGalleryView.as_view(), name='gallery_favorite'),
    path('explore/favorite/', FavoriteView.as_view(), name='explore_favorite'),
    
    path('gallery/profileposts/', ProfilePostGaleryView.as_view(), name='gallery_favorite'),
    path('explore/profileposts/', CurrentProfilePostExploreView.as_view(), name='explore_favorite'),
    
    path('gallery/otherprofileposts/<int:pk>/', CurrentProfilePostGalleryView.as_view(), name='gallery_favorite'),
    path('explore/otherprofileposts/<int:pk>/', ProfilePostExploreView.as_view(), name='explore_favorite'),

]
