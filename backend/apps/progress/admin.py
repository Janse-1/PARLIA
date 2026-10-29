from django.contrib import admin
from .models import LearningProgress


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'status', 'started_at', 'completed_at', 'updated_at')
    list_filter = ('status', 'lesson__module', 'updated_at')
    search_fields = ('user__email', 'lesson__title')
    readonly_fields = ('started_at', 'updated_at')
    ordering = ('-updated_at',)
