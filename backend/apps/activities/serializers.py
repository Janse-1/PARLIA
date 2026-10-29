from rest_framework import serializers
from .models import Activity, Question, ActivityAttempt, ActivityType


class QuestionPublicSerializer(serializers.ModelSerializer):
    """
    Expone el enunciado y las opciones ocultando el flag `is_correct` antes de que el estudiante responda.
    """
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'prompt_text',
            'options',
            'order',
        )

    def get_options(self, obj: Question):
        raw_options = obj.options_json if isinstance(obj.options_json, list) else []
        return [
            {
                'id': opt.get('id'),
                'text': opt.get('text', ''),
            }
            for opt in raw_options
            if isinstance(opt, dict)
        ]


class ActivityDetailSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    questions = QuestionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id',
            'lesson_id',
            'title',
            'description',
            'activity_type',
            'activity_type_display',
            'questions',
        )


class ActivityAttemptCreateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=False, allow_null=True)
    selected_option = serializers.IntegerField(required=False, allow_null=True)
    reflection_text = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        activity: Activity = self.context['activity']
        selected_option = attrs.get('selected_option')
        reflection_text = (attrs.get('reflection_text') or '').strip()

        if activity.activity_type == ActivityType.REFLECTION:
            if not reflection_text:
                raise serializers.ValidationError(
                    {'reflection_text': 'Por favor escribe tu reflexión técnica para continuar.'}
                )
        else:
            if selected_option is None and not reflection_text:
                raise serializers.ValidationError(
                    {'selected_option': 'Selecciona una opción o ingresa tu análisis técnico.'}
                )

        attrs['reflection_text'] = reflection_text if reflection_text else None
        return attrs


class ActivityAttemptSerializer(serializers.ModelSerializer):
    activity_id = serializers.IntegerField(source='activity.id', read_only=True)

    class Meta:
        model = ActivityAttempt
        fields = (
            'id',
            'activity_id',
            'selected_option',
            'reflection_text',
            'is_correct',
            'submitted_at',
        )
        read_only_fields = fields

