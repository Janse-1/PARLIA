from django.urls import path
from .views import ModuleListAPIView, ModuleDetailAPIView, LessonDetailAPIView

urlpatterns = [
    path('modules/', ModuleListAPIView.as_view(), name='module-list'),
    path('modules/<int:pk>/', ModuleDetailAPIView.as_view(), name='module-detail'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
]

