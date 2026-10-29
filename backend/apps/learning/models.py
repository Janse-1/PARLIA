from django.db import models


class AssetType(models.TextChoices):
    VIDEO_URL = 'video_url', 'Video Externo'
    IMAGE_URL = 'image_url', 'Imagen Externa'
    EXTERNAL_DOC = 'external_doc', 'Documento de Consulta'


class Module(models.Model):
    title = models.CharField('título del módulo', max_length=200)
    slug = models.SlugField('slug', max_length=220, unique=True, db_index=True)
    description = models.TextField('descripción y objetivos')
    order = models.PositiveIntegerField('orden secuencial', default=1, db_index=True)
    is_published = models.BooleanField('publicado', default=True, db_index=True)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de actualización', auto_now=True)

    class Meta:
        db_table = 'learning_module'
        ordering = ['order']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self) -> str:
        return f"Módulo {self.order}: {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='módulo',
    )
    title = models.CharField('título de la lección', max_length=200)
    slug = models.SlugField('slug', max_length=220)
    content = models.TextField('contenido pedagógico')
    estimated_minutes = models.PositiveIntegerField('tiempo estimado (minutos)', default=10)
    order = models.PositiveIntegerField('orden en el módulo', default=1)
    is_published = models.BooleanField('publicada', default=True, db_index=True)
    created_at = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('fecha de actualización', auto_now=True)

    class Meta:
        db_table = 'learning_lesson'
        ordering = ['module__order', 'order']
        constraints = [
            models.UniqueConstraint(
                fields=['module', 'order'],
                name='unique_module_lesson_order',
            )
        ]
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'

    def __str__(self) -> str:
        return f"[{self.module.order}.{self.order}] {self.title}"


class MediaAsset(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='media_assets',
        verbose_name='lección',
    )
    title = models.CharField('título descriptivo', max_length=150)
    asset_type = models.CharField(
        'tipo de recurso',
        max_length=20,
        choices=AssetType.choices,
        default=AssetType.VIDEO_URL,
    )
    url = models.URLField('enlace HTTPS externo', max_length=500)
    description = models.CharField(
        'nota contextual',
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'learning_mediaasset'
        verbose_name = 'Recurso Multimedia'
        verbose_name_plural = 'Recursos Multimedia'

    def __str__(self) -> str:
        return f"{self.title} ({self.get_asset_type_display()})"
