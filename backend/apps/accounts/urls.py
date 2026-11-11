from django.urls import path
from .views import LoginAPIView, LogoutAPIView, MeAPIView, RegisterAPIView

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),
    path('me/', MeAPIView.as_view(), name='auth-me'),
]
