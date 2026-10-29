from django.contrib import admin
from .models import Activity, Question, ActivityAttempt


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    ordering = ('order',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'activity_type')
    list_filter = ('activity_type', 'lesson__module')
    search_fields = ('title', 'description', 'lesson__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'activity', 'prompt_text')
    list_filter = ('activity__activity_type', 'activity__lesson__module')
    search_fields = ('prompt_text', 'explanation')
    ordering = ('activity', 'order')


@admin.register(ActivityAttempt)
class ActivityAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'selected_option', 'is_correct', 'submitted_at')
    list_filter = ('is_correct', 'activity__activity_type', 'submitted_at')
    search_fields = ('user__email', 'activity__title', 'reflection_text')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
