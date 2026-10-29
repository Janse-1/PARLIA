# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-10-28  

---

## 1. Estado Actual de la Implementación
* **Fases Completadas:**
  - Fase 1 (Inicialización del Entorno, Configuración Base y Conexiones) — 100%.
  - Fase 2 (Modelado de Datos, Migraciones y Panel de Administración) — 100% (`T2.1` a `T2.6` completadas).
* **Fase Activa:** Fase 3 (Desarrollo de la API REST `/api/v1/`).
* **Subtarea Siguiente:** T3.1 (Endpoints de Autenticación en `apps/accounts`).

---

## 2. Estado de Base de Datos y Django Admin
* **Tablas en MySQL (`parlia_db`):**
  - `accounts_user` (con los 7 programas: `Sistemas`, `Industrial`, `Mecanica`, `Civil`, `Ambiental`, `Energias`, `Otro`).
  - `learning_module`, `learning_lesson` (`unique_module_lesson_order`), `learning_mediaasset`.
  - `activities_activity`, `activities_question`, `activities_activityattempt`.
  - `progress_learningprogress` (`unique_user_lesson_progress`).
* **Superusuario Local:**
  - Correo: `admin@uniguajira.edu.co` / Username: `admin` / Contraseña local: `ParliaAdmin2026*`.
* **6 Módulos Oficiales Cargados en MySQL:**
  1. Fundamentos de la Inteligencia Artificial Generativa
  2. Ingeniería de Prompts
  3. Verificaciones
  4. Ética, Privacidad e Integridad Académica
  5. Aplicación en investigación, redacción
  6. Actividades finales

---

## 3. Próximos Pasos Inmediatos
1. Ejecutar **T3.1** (Endpoints de Autenticación en `apps/accounts`):
   - Crear serializers (`LoginSerializer`, `UserSerializer`).
   - Implementar vistas para `POST /api/v1/auth/login/`, `POST /api/v1/auth/logout/` y `GET /api/v1/me/` siguiendo el formato estándar de respuesta (`{"status": "success", "data": ...}` y `{"status": "error", "code": ..., "message": ..., "details": ...}`).
   - Conectar rutas en `apps/accounts/urls.py` y `config/urls.py`.
