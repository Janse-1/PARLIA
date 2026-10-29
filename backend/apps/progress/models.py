from django.conf import settings
from django.db import models
from apps.learning.models import Lesson


class ProgressStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    IN_PROGRESS = 'in_progress', 'En Progreso'
    COMPLETED = 'completed', 'Completada'


class LearningProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name='estudiante',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='student_progress',
        verbose_name='lección',
    )
    status = models.CharField(
        'estado de avance',
        max_length=20,
        choices=ProgressStatus.choices,
        default=ProgressStatus.IN_PROGRESS,
        db_index=True,
    )
    started_at = models.DateTimeField('fecha de inicio', auto_now_add=True)
    completed_at = models.DateTimeField('fecha de completitud', null=True, blank=True)
    updated_at = models.DateTimeField('última actualización', auto_now=True, db_index=True)

    class Meta:
        db_table = 'progress_learningprogress'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'lesson'],
                name='unique_user_lesson_progress',
            )
        ]
        verbose_name = 'Progreso de Aprendizaje'
        verbose_name_plural = 'Progresos de Aprendizaje'

    def __str__(self) -> str:
        return f"{self.user.email} - {self.lesson.title} [{self.status}]"
