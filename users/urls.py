from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('checkAuthenticated/', CheckAuthenticatedView.as_view(), name='checkAuthenticated_user'),
    path('feed/', HomeView.as_view(), name='feed_user'),
]