# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-10-28  

---

## 1. Estado Actual de la Implementación
* **Fases Completadas:**
  - Fase 1 (Inicialización del Entorno, Configuración Base y Conexiones) — 100%.
  - Fase 2 (Modelado de Datos, Migraciones y Panel de Administración) — 100%.
  - Fase 3 (Desarrollo de la API REST `/api/v1/`) — 100% (`T3.1` a `T3.5` completadas).
* **Fase Activa:** Fase 4 (Frontend Base - Layout, Navegación y Vistas de Estudio).
* **Subtarea Siguiente:** T4.1 (Sistema de Estilos y Tokens de Diseño en `frontend/src/styles/`).

---

## 2. Matriz Completa de Endpoints Activos (`/api/v1/`)
Todos los endpoints responden con formato estandarizado `{"status": "success", "data": ...}` o `{"status": "error", "code": "...", "message": "...", "details": ...}`:
* `POST /api/v1/auth/login/` (`AllowAny`): Autentica credenciales y devuelve `token` + perfil (`UserSerializer`).
* `POST /api/v1/auth/logout/` (`IsAuthenticated`): Revoca el token y cierra sesión.
* `GET /api/v1/me/` (`IsAuthenticated`): Información del estudiante activo extraída de `request.user`.
* `GET /api/v1/modules/` (`IsAuthenticated`): Los 6 módulos oficiales publicados con `lessons_count`.
* `GET /api/v1/modules/{id}/` (`IsAuthenticated`): Detalle de módulo con listado ordenado de lecciones.
* `GET /api/v1/lessons/{id}/` (`IsAuthenticated`): Contenido de lección, `media_assets`, `activity_id` y navegación anterior/siguiente.
* `GET /api/v1/progress/me/` (`IsAuthenticated`): Resumen global, avance por módulo y registros detallados de `request.user` (anti-IDOR).
* `POST` / `PATCH /api/v1/progress/` (`IsAuthenticated`): Upsert de estado (`in_progress`, `completed`) sin duplicados (`UniqueConstraint`).
* `GET /api/v1/activities/{id}/` (`IsAuthenticated`): Actividad y preguntas formativas ocultando `is_correct` antes de responder.
* `POST /api/v1/activities/{id}/attempts/` (`IsAuthenticated`): Registra intento formativo no punitivo para `request.user` y devuelve retroalimentación inmediata (`title`, `is_correct`, `explanation`).

---

## 3. Próximos Pasos Inmediatos
1. Ejecutar **T4.1** (Sistema de Estilos y Tokens de Diseño):
   - Crear `frontend/src/styles/variables.css` con la paleta institucional de Uniguajira (`#C2822B` Ocre Tierra, `#2A9D8F` Aguamarina Caribe, `#E76F51` Rosa Flamenco/Coral, superficies `#F8F9FA`, `#FFFFFF`, texto `#1F2937`, `#6B7280`, éxito `#10B981`).
   - Crear `frontend/src/styles/main.css` con tipografía `'Inter'`, reset CSS limpio, utilidades de layout y soporte a `@media (prefers-reduced-motion: reduce)`.
