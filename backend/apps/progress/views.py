from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.learning.models import Module, Lesson
from .models import LearningProgress, ProgressStatus
from .serializers import LearningProgressSerializer, ProgressUpsertSerializer


class MyProgressAPIView(APIView):
    """
    GET /api/v1/progress/me/
    Devuelve el resumen global y detallado del progreso del estudiante autenticado (request.user).
    Prevención estricta de IDOR: ignora cualquier user_id externo.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Registros de progreso del estudiante autenticado
        progress_records = (
            LearningProgress.objects.filter(
                user=user,
                lesson__is_published=True,
                lesson__module__is_published=True,
            )
            .select_related('lesson', 'lesson__module')
            .order_by('lesson__module__order', 'lesson__order')
        )

        status_by_lesson = {rec.lesson_id: rec.status for rec in progress_records}

        # Cálculo de avance por cada uno de los módulos publicados
        modules = (
            Module.objects.filter(is_published=True)
            .prefetch_related('lessons')
            .order_by('order')
        )

        modules_summary = []
        total_lessons = 0
        total_completed = 0

        for mod in modules:
            published_lessons = [l for l in mod.lessons.all() if l.is_published]
            mod_total = len(published_lessons)
            mod_completed = sum(
                1 for l in published_lessons
                if status_by_lesson.get(l.id) == ProgressStatus.COMPLETED
            )
            mod_in_progress = sum(
                1 for l in published_lessons
                if status_by_lesson.get(l.id) == ProgressStatus.IN_PROGRESS
            )
            mod_pct = round((mod_completed / mod_total) * 100, 1) if mod_total > 0 else 0.0

            if mod_total > 0 and mod_completed == mod_total:
                mod_status = ProgressStatus.COMPLETED
            elif mod_completed > 0 or mod_in_progress > 0:
                mod_status = ProgressStatus.IN_PROGRESS
            else:
                mod_status = ProgressStatus.PENDING

            modules_summary.append({
                'module_id': mod.id,
                'order': mod.order,
                'title': mod.title,
                'slug': mod.slug,
                'total_lessons': mod_total,
                'completed_lessons': mod_completed,
                'percentage': mod_pct,
                'status': mod_status,
            })

            total_lessons += mod_total
            total_completed += mod_completed

        overall_percentage = (
            round((total_completed / total_lessons) * 100, 1)
            if total_lessons > 0
            else 0.0
        )

        serializer = LearningProgressSerializer(progress_records, many=True)

        return Response(
            {
                'status': 'success',
                'data': {
                    'total_lessons': total_lessons,
                    'completed_lessons': total_completed,
                    'overall_percentage': overall_percentage,
                    'modules': modules_summary,
                    'records': serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )


class ProgressUpsertAPIView(APIView):
    """
    POST / PATCH /api/v1/progress/
    Registra o actualiza el estado de una lección para request.user sin duplicados.
    """
    permission_classes = [IsAuthenticated]

    def _upsert(self, request):
        serializer = ProgressUpsertSerializer(data=request.data, context={})
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'code': 'VALIDATION_ERROR',
                    'message': 'Datos de progreso inválidos.',
                    'details': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        lesson = serializer.context['lesson']
        new_status = serializer.validated_data['status']

        defaults = {'status': new_status}
        if new_status == ProgressStatus.COMPLETED:
            defaults['completed_at'] = timezone.now()

        # Si ya estaba completada y se vuelve a abrir como in_progress, preservamos completed
        existing = LearningProgress.objects.filter(user=request.user, lesson=lesson).first()
        if existing and existing.status == ProgressStatus.COMPLETED and new_status == ProgressStatus.IN_PROGRESS:
            record = existing
            created = False
        else:
            record, created = LearningProgress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults=defaults,
            )

        return Response(
            {
                'status': 'success',
                'data': LearningProgressSerializer(record).data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def post(self, request):
        return self._upsert(request)

    def patch(self, request):
        return self._upsert(request)
