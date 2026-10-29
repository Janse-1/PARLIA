from django.conf import settings
from django.db import models
from apps.learning.models import Lesson


class ActivityType(models.TextChoices):
    MULTIPLE_CHOICE = 'multiple_choice', 'Selección Múltiple'
    REFLECTION = 'reflection', 'Pregunta de Reflexión'
    PROMPT_AUDIT = 'prompt_audit', 'Auditoría de Prompt/Respuesta'


class Activity(models.Model):
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='activity',
        verbose_name='lección',
    )
    title = models.CharField('título de la actividad', max_length=200)
    description = models.TextField('instrucciones para el estudiante')
    activity_type = models.CharField(
        'tipo de actividad',
        max_length=30,
        choices=ActivityType.choices,
        default=ActivityType.MULTIPLE_CHOICE,
    )

    class Meta:
        db_table = 'activities_activity'
        verbose_name = 'Actividad Formativa'
        verbose_name_plural = 'Actividades Formativas'

    def __str__(self) -> str:
        return f"{self.title} ({self.get_activity_type_display()})"


class Question(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='actividad',
    )
    prompt_text = models.TextField('enunciado de la pregunta')
    options_json = models.JSONField(
        'opciones JSON',
        default=list,
        blank=True,
    )
    explanation = models.TextField('explicación formativa')
    order = models.PositiveIntegerField('orden de presentación', default=1)

    class Meta:
        db_table = 'activities_question'
        ordering = ['order']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self) -> str:
        return f"Pregunta {self.order} - {self.activity.title}"


class ActivityAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_attempts',
        verbose_name='estudiante',
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='actividad',
    )
    selected_option = models.IntegerField(
        'opción seleccionada',
        null=True,
        blank=True,
    )
    reflection_text = models.TextField(
        'texto de reflexión',
        null=True,
        blank=True,
    )
    is_correct = models.BooleanField(
        'es correcta',
        null=True,
        blank=True,
    )
    submitted_at = models.DateTimeField(
        'fecha de envío',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = 'activities_activityattempt'
        ordering = ['-submitted_at']
        verbose_name = 'Intento de Actividad'
        verbose_name_plural = 'Intentos de Actividades'

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.activity.title} ({self.submitted_at:%Y-%m-%d %H:%M})"
