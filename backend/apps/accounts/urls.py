from django.urls import path
from .views import LoginAPIView, LogoutAPIView, MeAPIView

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),
    path('me/', MeAPIView.as_view(), name='auth-me'),
]

