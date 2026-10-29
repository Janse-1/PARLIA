from rest_framework import serializers
from apps.learning.models import Lesson
from .models import LearningProgress, ProgressStatus


class LearningProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    module_id = serializers.IntegerField(source='lesson.module_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LearningProgress
        fields = (
            'id',
            'lesson_id',
            'lesson_title',
            'module_id',
            'status',
            'status_display',
            'started_at',
            'completed_at',
            'updated_at',
        )
        read_only_fields = fields


class ProgressUpsertSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(
        choices=[ProgressStatus.IN_PROGRESS, ProgressStatus.COMPLETED],
        default=ProgressStatus.IN_PROGRESS,
    )

    def validate_lesson_id(self, value: int):
        try:
            lesson = Lesson.objects.select_related('module').get(
                pk=value,
                is_published=True,
                module__is_published=True,
            )
        except Lesson.DoesNotExist:
            raise serializers.ValidationError('La lección especificada no existe o no está publicada.')
        self.context['lesson'] = lesson
        return value

