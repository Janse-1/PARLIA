# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-10-28  

---

## 1. Estado Actual de la Implementación
* **Fase Completada:** Fase 1 (Inicialización del Entorno, Configuración Base y Conexiones) — 100%.
* **Fase Activa:** Fase 2 (Modelado de Datos, Migraciones y Panel de Administración).
* **Subtareas Completadas en Fase 2:**
  - T2.1 (Modelo de Usuario en `apps/accounts`).
  - T2.2 (Modelos de Aprendizaje en `apps/learning`).
* **Subtarea Siguiente:** T2.3 (Modelos de Actividades en `apps/activities`).

---

## 2. Modelos Implementados
* **`apps.accounts.models.User`** (tabla `accounts_user`):
  - Extiende `AbstractUser` (`USERNAME_FIELD = 'email'`).
  - `program`: `Sistemas`, `Industrial`, `Mecanica`, `Civil`, `Ambiental`, `Energias`, `Otro`.
* **`apps.learning.models`:**
  - `Module` (tabla `learning_module`): `title`, `slug` (único), `description`, `order`, `is_published`, `created_at`, `updated_at`.
  - `Lesson` (tabla `learning_lesson`): `module` (FK), `title`, `slug`, `content`, `estimated_minutes`, `order`, `is_published`, `created_at`, `updated_at`, con `UniqueConstraint(fields=['module', 'order'], name='unique_module_lesson_order')`.
  - `MediaAsset` (tabla `learning_mediaasset`): `lesson` (FK), `title`, `asset_type` (`video_url`, `image_url`, `external_doc`), `url`, `description`.

---

## 3. Próximos Pasos Inmediatos
1. Ejecutar **T2.3** (Modelos de Actividades en `apps/activities`):
   - `ActivityType` (`multiple_choice`, `reflection`, `prompt_audit`).
   - `Activity` (`lesson` OneToOneField, `title`, `description`, `activity_type`).
   - `Question` (`activity` FK, `prompt_text`, `options_json`, `explanation`, `order`).
   - `ActivityAttempt` (`user` FK, `activity` FK, `selected_option`, `reflection_text`, `is_correct`, `submitted_at`).
