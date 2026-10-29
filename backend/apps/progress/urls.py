from django.urls import path
from .views import MyProgressAPIView, ProgressUpsertAPIView

urlpatterns = [
    path('progress/me/', MyProgressAPIView.as_view(), name='progress-me'),
    path('progress/', ProgressUpsertAPIView.as_view(), name='progress-upsert'),
]

