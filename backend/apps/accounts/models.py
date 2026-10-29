from django.contrib.auth.models import AbstractUser
from django.db import models


class AcademicProgram(models.TextChoices):
    SISTEMAS = 'Sistemas', 'Ingeniería de Sistemas'
    INDUSTRIAL = 'Industrial', 'Ingeniería Industrial'
    MECANICA = 'Mecanica', 'Ingeniería Mecánica'
    CIVIL = 'Civil', 'Ingeniería Civil'
    AMBIENTAL = 'Ambiental', 'Ingeniería Ambiental'
    ENERGIAS = 'Energias', 'Ingeniería en Energías'
    OTRO = 'Otro', 'Otro Programa'


class User(AbstractUser):
    email = models.EmailField(
        'correo electrónico institucional',
        max_length=254,
        unique=True,
        db_index=True,
    )
    program = models.CharField(
        'programa académico',
        max_length=100,
        choices=AcademicProgram.choices,
        default=AcademicProgram.SISTEMAS,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self) -> str:
        return f"{self.email} ({self.get_program_display()})"
