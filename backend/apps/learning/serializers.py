from rest_framework import serializers
from .models import Module, Lesson, MediaAsset


class MediaAssetSerializer(serializers.ModelSerializer):
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)

    class Meta:
        model = MediaAsset
        fields = (
            'id',
            'title',
            'asset_type',
            'asset_type_display',
            'url',
            'description',
        )


class LessonSummarySerializer(serializers.ModelSerializer):
    has_activity = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'module_id',
            'title',
            'slug',
            'estimated_minutes',
            'order',
            'has_activity',
        )

    def get_has_activity(self, obj: Lesson) -> bool:
        return hasattr(obj, 'activity')


class LessonDetailSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_order = serializers.IntegerField(source='module.order', read_only=True)
    media_assets = MediaAssetSerializer(many=True, read_only=True)
    activity_id = serializers.SerializerMethodField()
    previous_lesson_id = serializers.SerializerMethodField()
    next_lesson_id = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'id',
            'module_id',
            'module_title',
            'module_order',
            'title',
            'slug',
            'content',
            'estimated_minutes',
            'order',
            'media_assets',
            'activity_id',
            'previous_lesson_id',
            'next_lesson_id',
            'updated_at',
        )

    def get_activity_id(self, obj: Lesson):
        return obj.activity.id if hasattr(obj, 'activity') else None

    def get_previous_lesson_id(self, obj: Lesson):
        prev_lesson = (
            Lesson.objects.filter(
                module_id=obj.module_id,
                is_published=True,
                order__lt=obj.order,
            )
            .order_by('-order')
            .values_list('id', flat=True)
            .first()
        )
        return prev_lesson

    def get_next_lesson_id(self, obj: Lesson):
        next_lesson = (
            Lesson.objects.filter(
                module_id=obj.module_id,
                is_published=True,
                order__gt=obj.order,
            )
            .order_by('order')
            .values_list('id', flat=True)
            .first()
        )
        return next_lesson


class ModuleListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Module
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'order',
            'lessons_count',
        )


class ModuleDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'order',
            'lessons',
        )

