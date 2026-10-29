# DATA DICTIONARY: Especificación y Modelo de Datos Relacional

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Motor de Persistencia:** MySQL 8.0+ (Motor InnoDB, Charset `utf8mb4`, Collation `utf8mb4_unicode_ci`)  
**ORM:** Django ORM 5.1+  
**Versión:** 1.0 (MVP 1 Semana)

---

## 1. Diagrama Entidad-Relación Lógico (DER)

```text
       +-----------------------+
       |   accounts_user       |
       +-----------------------+
       | PK  id                |
       |     email (UQ)        |<--------------+
       |     username (UQ)     |               |
       |     password          |               |
       +-----------------------+               |
                   |                           |
                   | 1:N                       | 1:N
                   v                           |
       +-----------------------+   +-----------------------+
       | progress_             |   | activities_           |
       | learningprogress      |   | activityattempt       |
       +-----------------------+   +-----------------------+
       | PK  id                |   | PK  id                |
       | FK  user_id           |   | FK  user_id           |
       | FK  lesson_id         |   | FK  activity_id       |
       |     status            |   |     selected_option   |
       |     completed_at      |   |     reflection_text   |
       | UQ(user_id,lesson_id) |   |     is_correct        |
       +-----------------------+   |     submitted_at      |
                   ^               +-----------------------+
                   | 1:N                       ^
                   |                           | 1:N
       +-----------------------+               |
       |   learning_module     |               |
       +-----------------------+               |
       | PK  id                |               |
       |     title             |               |
       |     order             |               |
       +-----------------------+               |
                   |                           |
                   | 1:N                       |
                   v                           |
       +-----------------------+   +-----------------------+
       |   learning_lesson     |   | activities_activity   |
       +-----------------------+   +-----------------------+
       | PK  id                |   | PK  id                |
       | FK  module_id         |-->| FK  lesson_id (1:1)   |
       |     title             |   |     title             |
       |     order             |   |     activity_type     |
       +-----------------------+   +-----------------------+
                   |                           |
                   | 1:N                       | 1:N
                   v                           v
       +-----------------------+   +-----------------------+
       | learning_mediaasset   |   | activities_question   |
       +-----------------------+   +-----------------------+
       | PK  id                |   | PK  id                |
       | FK  lesson_id         |   | FK  activity_id       |
       |     asset_type        |   |     prompt_text       |
       |     url               |   |     options_json      |
       +-----------------------+   +-----------------------+
```

---

## 2. Especificación de Tablas por Aplicación

### 2.1. Aplicación: `accounts` (Autenticación y Perfiles)

#### Tabla: `accounts_user`
Representa la cuenta de acceso del estudiante o administrador del laboratorio. Extiende `AbstractUser` de Django para operar de forma primaria con correo electrónico institucional.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador único del usuario. |
| `email` | `VARCHAR(254)` | `EmailField` | NO | N/A | `UNIQUE`, `INDEX` | Correo institucional (`@uniguajira.edu.co`). |
| `username` | `VARCHAR(150)` | `CharField` | NO | N/A | `UNIQUE` | Identificador alfanumérico único para URL o login secundario. |
| `first_name`| `VARCHAR(150)` | `CharField` | NO | `""` | Ninguna | Nombres del estudiante. |
| `last_name` | `VARCHAR(150)` | `CharField` | NO | `""` | Ninguna | Apellidos del estudiante. |
| `password` | `VARCHAR(128)` | `CharField` | NO | N/A | Ninguna | Hash seguro de contraseña (formato PBKDF2/Argon2). |
| `program` | `VARCHAR(100)` | `CharField` | NO | `'Sistemas'` | Ninguna | Programa académico: `'Sistemas'`, `'Industrial'`, `'Otro'`. |
| `is_active` | `TINYINT(1)` | `BooleanField`| NO | `1` | Ninguna | Bandera que habilita o suspende la cuenta. |
| `is_staff` | `TINYINT(1)` | `BooleanField`| NO | `0` | Ninguna | Permite acceso al panel de Django Admin. |
| `date_joined`| `DATETIME(6)` | `DateTimeField`| NO | `CURRENT_TIMESTAMP` | Ninguna | Fecha y hora de creación de la cuenta. |

---

### 2.2. Aplicación: `learning` (Contenido Pedagógico)

#### Tabla: `learning_module`
Catálogo de los 6 ejes formativos en Inteligencia Artificial Generativa.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador único del módulo. |
| `title` | `VARCHAR(200)` | `CharField` | NO | N/A | Ninguna | Nombre oficial del módulo pedagógico. |
| `slug` | `VARCHAR(220)` | `SlugField` | NO | N/A | `UNIQUE`, `INDEX` | Identificador semántico para URLs limpias. |
| `description`| `LONGTEXT` | `TextField` | NO | N/A | Ninguna | Resumen y objetivos de competencia del módulo. |
| `order` | `INT UNSIGNED` | `PositiveIntegerField` | NO | `1` | `INDEX` | Posición secuencial de despliegue (1 al 6). |
| `is_published`| `TINYINT(1)` | `BooleanField` | NO | `1` | `INDEX` | Determina si el módulo está disponible a estudiantes. |
| `created_at`| `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP` | Ninguna | Marca temporal de creación. |
| `updated_at`| `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP ON UPDATE` | Ninguna | Marca temporal de última modificación. |

---

#### Tabla: `learning_lesson`
Unidad de aprendizaje o subtema perteneciente a un módulo formativo.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador único de la lección. |
| `module_id` | `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`learning_module.id`), `ON DELETE CASCADE`, `INDEX` | Módulo al que pertenece la lección. |
| `title` | `VARCHAR(200)` | `CharField` | NO | N/A | Ninguna | Título de la lección. |
| `slug` | `VARCHAR(220)` | `SlugField` | NO | N/A | Ninguna | Identificador amigable para rutas web. |
| `content` | `LONGTEXT` | `TextField` | NO | N/A | Ninguna | Cuerpo educativo en formato estructurado (HTML seguro/Markdown). |
| `estimated_minutes` | `INT UNSIGNED` | `PositiveIntegerField` | NO | `10` | Ninguna | Tiempo sugerido de lectura y práctica en minutos. |
| `order` | `INT UNSIGNED` | `PositiveIntegerField` | NO | `1` | Ninguna | Orden relativo dentro del módulo. |
| `is_published`| `TINYINT(1)` | `BooleanField` | NO | `1` | `INDEX` | Estado de visibilidad para los estudiantes. |
| `created_at`| `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP` | Ninguna | Fecha de registro. |
| `updated_at`| `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP ON UPDATE` | Ninguna | Última actualización. |

* **Restricción de Unicidad:** `UNIQUE (module_id, order)` para evitar colisiones en la secuencia de lecciones.

---

#### Tabla: `learning_mediaasset`
Registro de referencias externas a recursos multimedia (videos en plataformas especializadas, diagramas e infografías). No almacena archivos binarios directamente.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador del recurso multimedia. |
| `lesson_id` | `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`learning_lesson.id`), `ON DELETE CASCADE`, `INDEX` | Lección asociada al recurso. |
| `title` | `VARCHAR(150)` | `CharField` | NO | N/A | Ninguna | Título descriptivo o texto alternativo (a11y). |
| `asset_type`| `VARCHAR(20)` | `CharField` | NO | `'video_url'` | Ninguna | Categoría: `'video_url'`, `'image_url'`, `'external_doc'`. |
| `url` | `VARCHAR(500)` | `URLField` | NO | N/A | Ninguna | Enlace absoluto seguro (HTTPS) hacia el archivo o video. |
| `description`| `VARCHAR(255)`| `CharField` | SÍ | `NULL` | Ninguna | Nota contextual complementaria. |

---

### 2.3. Aplicación: `activities` (Evaluación Formativa y Reflexión)

#### Tabla: `activities_activity`
Contenedor de actividad asociado de manera unívoca a una lección.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador de la actividad. |
| `lesson_id` | `BIGINT` | `OneToOneField` | NO | N/A | `UNIQUE`, `FOREIGN KEY` (`learning_lesson.id`), `ON DELETE CASCADE` | Relación 1:1 estricta con la lección. |
| `title` | `VARCHAR(200)` | `CharField` | NO | N/A | Ninguna | Nombre del ejercicio o reto formativo. |
| `description`| `LONGTEXT` | `TextField` | NO | N/A | Ninguna | Instrucciones detalladas para el estudiante. |
| `activity_type` | `VARCHAR(30)` | `CharField` | NO | `'multiple_choice'` | Ninguna | Tipo: `'multiple_choice'`, `'reflection'`, `'prompt_audit'`. |

---

#### Tabla: `activities_question`
Pregunta o ítem específico perteneciente a una actividad de selección múltiple o auditoría de respuestas.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador único de la pregunta. |
| `activity_id`| `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`activities_activity.id`), `ON DELETE CASCADE`, `INDEX` | Actividad que contiene la pregunta. |
| `prompt_text`| `LONGTEXT` | `TextField` | NO | N/A | Ninguna | Enunciado de la pregunta, fragmento de código o caso. |
| `options_json`| `JSON` | `JSONField` | NO | N/A | Ninguna | Estructura JSON con opciones: `[{"id": 1, "text": "...", "is_correct": true}]`. |
| `explanation`| `LONGTEXT` | `TextField` | NO | N/A | Ninguna | Retroalimentación técnica explicativa tras responder. |
| `order` | `INT UNSIGNED` | `PositiveIntegerField` | NO | `1` | Ninguna | Secuencia de presentación en la vista. |

---

#### Tabla: `activities_activityattempt`
Registro de participación no punitiva del estudiante en los ejercicios.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador del intento. |
| `user_id` | `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`accounts_user.id`), `ON DELETE CASCADE`, `INDEX` | Estudiante que realiza el intento. |
| `activity_id`| `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`activities_activity.id`), `ON DELETE CASCADE`, `INDEX` | Actividad evaluada. |
| `selected_option` | `INT` | `IntegerField` | SÍ | `NULL` | Ninguna | ID de la opción elegida en preguntas de opción múltiple. |
| `reflection_text`| `LONGTEXT` | `TextField` | SÍ | `NULL` | Ninguna | Texto ingresado en actividades abiertas o de autoevaluación. |
| `is_correct` | `TINYINT(1)` | `BooleanField` | SÍ | `NULL` | Ninguna | Evaluación formativa automática (`NULL` si es reflexión). |
| `submitted_at`| `DATETIME(6)` | `DateTimeField`| NO | `CURRENT_TIMESTAMP` | `INDEX` | Marca de tiempo del intento. |

---

### 2.4. Aplicación: `progress` (Seguimiento y Estado de Avance)

#### Tabla: `progress_learningprogress`
Tabla central para registrar el estado de cada lección por estudiante. Garantiza cero duplicados mediante clave compuesta única.

| Campo | Tipo MySQL | Tipo Django | Nulo | Por Defecto | Restricciones / Índices | Descripción |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT AUTO_INCREMENT` | `BigAutoField` | NO | N/A | `PRIMARY KEY` | Identificador único del registro de progreso. |
| `user_id` | `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`accounts_user.id`), `ON DELETE CASCADE` | Estudiante asociado. |
| `lesson_id` | `BIGINT` | `ForeignKey` | NO | N/A | `FOREIGN KEY` (`learning_lesson.id`), `ON DELETE CASCADE` | Lección correspondiente. |
| `status` | `VARCHAR(20)` | `CharField` | NO | `'in_progress'` | `INDEX` | Estados: `'pending'`, `'in_progress'`, `'completed'`. |
| `started_at` | `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP` | Ninguna | Momento en que el estudiante abrió la lección. |
| `completed_at`| `DATETIME(6)`| `DateTimeField` | SÍ | `NULL` | Ninguna | Momento exacto en que completó la actividad o lectura. |
| `updated_at` | `DATETIME(6)` | `DateTimeField` | NO | `CURRENT_TIMESTAMP ON UPDATE` | `INDEX` | Fecha de última sincronización. |

* **Restricción Única Obligatoria (CRITICAL):**  
  `UNIQUE KEY uq_user_lesson (user_id, lesson_id)`  
  Impide que un mismo usuario tenga múltiples registros para la misma lección. Las actualizaciones de estado se efectúan vía sentencia `UPDATE` o `update_or_create()`.

---

## 3. Catálogo de Valores Enumerados (Choices)

Para estandarizar los valores en la base de datos y evitar inconsistencias por cadenas arbitrarias:

```python
# apps/accounts/models.py
class AcademicProgram(models.TextChoices):
    SISTEMAS = 'Sistemas', 'Ingeniería de Sistemas'
    INDUSTRIAL = 'Industrial', 'Ingeniería Industrial'
    OTRO = 'Otro', 'Otro Programa'

# apps/learning/models.py
class AssetType(models.TextChoices):
    VIDEO_URL = 'video_url', 'Video Externo'
    IMAGE_URL = 'image_url', 'Imagen Externa'
    EXTERNAL_DOC = 'external_doc', 'Documento de Consulta'

# apps/activities/models.py
class ActivityType(models.TextChoices):
    MULTIPLE_CHOICE = 'multiple_choice', 'Selección Múltiple'
    REFLECTION = 'reflection', 'Pregunta de Reflexión'
    PROMPT_AUDIT = 'prompt_audit', 'Auditoría de Prompt/Respuesta'

# apps/progress/models.py
class ProgressStatus(models.TextChoices):
    PENDING = 'pending', 'Pendiente'
    IN_PROGRESS = 'in_progress', 'En Progreso'
    COMPLETED = 'completed', 'Completada'
```

---

## 4. Definición de Modelos en Django (Referencia Técnica)

```python
# apps/progress/models.py
from django.db import models
from django.conf import settings
from apps.learning.models import Lesson

class LearningProgress(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        IN_PROGRESS = 'in_progress', 'En Progreso'
        COMPLETED = 'completed', 'Completada'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
        db_index=True
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'progress_learningprogress'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'lesson'],
                name='unique_user_lesson_progress'
            )
        ]
        verbose_name = 'Progreso de Aprendizaje'
        verbose_name_plural = 'Progresos de Aprendizaje'

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title} [{self.status}]"
```

---

## 5. Estrategia de Índices y Optimización de Consultas

1. **Índices en Claves Foráneas:** Todo campo `ForeignKey` en Django genera índice B-Tree automático en MySQL, optimizando las consultas `JOIN` entre lecciones, módulos y progreso.
2. **Índice para Ordenamiento:** Los campos `order` en `learning_module` y `learning_lesson` poseen índices para acelerar la recuperación ordenada del árbol de contenidos sin costo excesivo en CPU.
3. **Optimización N+1:** Las consultas de API que devuelvan módulos con progreso deben emplear `select_related('module')` y `prefetch_related('lessons')` desde los controladores DRF.

---

## 6. Procedimiento de Migración Inicial

Para aplicar este diccionario de datos de forma reproducible en el entorno de desarrollo:

1. Crear la base de datos en MySQL local con codificación estándar:
   ```sql
   CREATE DATABASE parlia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Configurar las credenciales en `backend/.env`.
3. Ejecutar las migraciones en el orden de dependencia de las aplicaciones:
   ```bash
   python manage.py makemigrations accounts learning activities progress
   python manage.py migrate
   ```
4. Crear superusuario para poblar los 6 módulos vía Django Admin:
   ```bash
   python manage.py createsuperuser
   ```