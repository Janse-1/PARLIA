from django.contrib import admin
from .models import Module, Lesson, MediaAsset


class MediaAssetInline(admin.TabularInline):
    model = MediaAsset
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'slug', 'is_published', 'updated_at')
    list_display_links = ('title',)
    list_editable = ('order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('module', 'order', 'title', 'estimated_minutes', 'is_published', 'updated_at')
    list_display_links = ('title',)
    list_filter = ('module', 'is_published')
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('module__order', 'order')
    inlines = [MediaAssetInline]


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'asset_type', 'url')
    list_filter = ('asset_type', 'lesson__module')
    search_fields = ('title', 'description', 'url')
