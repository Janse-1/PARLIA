from django.urls import path
from .views import ActivityDetailAPIView, ActivityAttemptCreateAPIView

urlpatterns = [
    path('activities/<int:pk>/', ActivityDetailAPIView.as_view(), name='activity-detail'),
    path('activities/<int:pk>/attempts/', ActivityAttemptCreateAPIView.as_view(), name='activity-attempts'),
]

