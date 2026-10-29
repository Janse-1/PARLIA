from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, ActivityAttempt, ActivityType
from .serializers import (
    ActivityDetailSerializer,
    ActivityAttemptCreateSerializer,
    ActivityAttemptSerializer,
)


class ActivityDetailAPIView(APIView):
    """
    GET /api/v1/activities/{id}/
    Devuelve la actividad formativa y sus preguntas sin revelar la respuesta correcta por adelantado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        activity = get_object_or_404(
            Activity.objects.select_related('lesson', 'lesson__module')
            .prefetch_related('questions')
            .filter(lesson__is_published=True, lesson__module__is_published=True),
            pk=pk,
        )
        serializer = ActivityDetailSerializer(activity)
        return Response(
            {
                'status': 'success',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ActivityAttemptCreateAPIView(APIView):
    """
    POST /api/v1/activities/{id}/attempts/
    Registra un intento formativo no punitivo para request.user y devuelve la explicación técnica inmediata.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int):
        activity = get_object_or_404(
            Activity.objects.select_related('lesson', 'lesson__module')
            .prefetch_related('questions')
            .filter(lesson__is_published=True, lesson__module__is_published=True),
            pk=pk,
        )

        serializer = ActivityAttemptCreateSerializer(
            data=request.data,
            context={'activity': activity},
        )
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'code': 'VALIDATION_ERROR',
                    'message': 'Datos del intento formativo incompletos.',
                    'details': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        question_id = serializer.validated_data.get('question_id')
        selected_option = serializer.validated_data.get('selected_option')
        reflection_text = serializer.validated_data.get('reflection_text')

        questions = list(activity.questions.all())
        target_question = None
        if question_id is not None:
            target_question = next((q for q in questions if q.id == question_id), None)
        if target_question is None and questions:
            target_question = questions[0]

        is_correct = None
        explanation = 'Gracias por compartir tu análisis reflexivo. Contrastar tus ideas fortalece tu criterio en ingeniería.'

        if target_question:
            explanation = target_question.explanation
            if activity.activity_type != ActivityType.REFLECTION and selected_option is not None:
                options = target_question.options_json if isinstance(target_question.options_json, list) else []
                matched_opt = next(
                    (opt for opt in options if isinstance(opt, dict) and opt.get('id') == selected_option),
                    None,
                )
                is_correct = bool(matched_opt.get('is_correct')) if matched_opt else False

        attempt = ActivityAttempt.objects.create(
            user=request.user,
            activity=activity,
            selected_option=selected_option,
            reflection_text=reflection_text,
            is_correct=is_correct,
        )

        if is_correct is True:
            feedback_title = '¡Excelente criterio técnico!'
        elif is_correct is False:
            feedback_title = 'Buen intento de exploración — Analicemos por qué:'
        else:
            feedback_title = 'Reflexión registrada en tu bitácora de aprendizaje'

        return Response(
            {
                'status': 'success',
                'data': {
                    'attempt': ActivityAttemptSerializer(attempt).data,
                    'feedback': {
                        'title': feedback_title,
                        'is_correct': is_correct,
                        'explanation': explanation,
                    },
                },
            },
            status=status.HTTP_201_CREATED,
        )
