from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Module, Lesson
from .serializers import (
    ModuleListSerializer,
    ModuleDetailSerializer,
    LessonDetailSerializer,
)


class ModuleListAPIView(APIView):
    """
    GET /api/v1/modules/
    Lista los 6 módulos oficiales publicados con el conteo de lecciones activas.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        modules = (
            Module.objects.filter(is_published=True)
            .annotate(
                lessons_count=Count('lessons', filter=Q(lessons__is_published=True))
            )
            .order_by('order')
        )
        serializer = ModuleListSerializer(modules, many=True)
        return Response(
            {
                'status': 'success',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ModuleDetailAPIView(APIView):
    """
    GET /api/v1/modules/{id}/
    Devuelve el detalle de un módulo junto con sus lecciones publicadas ordenadas.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        published_lessons = Prefetch(
            'lessons',
            queryset=Lesson.objects.filter(is_published=True)
            .select_related('activity')
            .order_by('order'),
        )
        module = get_object_or_404(
            Module.objects.filter(is_published=True).prefetch_related(published_lessons),
            pk=pk,
        )
        serializer = ModuleDetailSerializer(module)
        return Response(
            {
                'status': 'success',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class LessonDetailAPIView(APIView):
    """
    GET /api/v1/lessons/{id}/
    Devuelve el contenido pedagógico estructurado de una lección y sus recursos multimedia.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        lesson = get_object_or_404(
            Lesson.objects.filter(is_published=True, module__is_published=True)
            .select_related('module', 'activity')
            .prefetch_related('media_assets'),
            pk=pk,
        )
        serializer = LessonDetailSerializer(lesson)
        return Response(
            {
                'status': 'success',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )
