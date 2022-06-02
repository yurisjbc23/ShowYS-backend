from django.urls import path
from .views import *

urlpatterns = [
    path('create/user/', CreateUser.as_view(), name = 'user_create'),
    path('create/profile/', CreateProfile.as_view(), name = 'profile_create'),
    path('follow/unfollow/user/<int:pk>/', FollowUnfollow.as_view(), name = 'follows_create_delete'),
    path('profile/detail/user/', MyProfileRetrieve.as_view(), name = 'profile_detail'),
    path('profile/detail/user/<int:pk>/', OtherProfileRetrieve.as_view(), name = 'other_profile_detail'),
    path('update/profile/', MyProfileUpdate.as_view(), name = 'my_profile_detail_update'),
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('checkAuthenticated/', CheckAuthenticatedView.as_view(), name='checkAuthenticated_user'),
    path('feed/', HomeView.as_view(), name='feed_user'),
]