# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-11-10  

---

## 1. Estado Actual de la Implementación
* **Fases Completadas:** Fases 1 a 6 — 100% (`[x]`).
* **Fase en Pausa:** Fase 7 (Se ejecutará al finalizar todas las correcciones de la Fase 8).
* **Fase Activa:** Fase 8 (Rediseño Visual, Portal de Bienvenida CRM-Hero, Temas y Experiencia Refinada).
* **Subtareas Completadas en Fase 8:**
  - T8.1.1 (Reconfiguración de rutas en `router/index.js`: `/` usa `layout: 'landing'` sin mostrar Sidebar/Topbar internos ni módulos/carreras antes de iniciar sesión; todas las rutas internas exigen `requiresAuth: true`).
  - T8.1.2 (Rediseño completo de `HomeView.vue` inspirado en la estética espacial de Voxel con video de fondo local `gemini_generated_video_0609d70b.mp4`, sección interactiva de scroll-linked timeline con Anime.js sobre `para_animar.jpeg`, secciones `#synapse`, `#technology`, `#system`, `#vision`, `#demo`, `#horizon` y selector bilingüe `EN | ES`).
* **Subtarea Siguiente:** Bloque 8.2 (`T8.2.1` y `T8.2.2` - Registro de Nuevos Estudiantes Self-Service en Backend y Frontend).

---

## 2. Próximos Pasos Inmediatos
1. Ejecutar **T8.2.1** y **T8.2.2**:
   - En `backend/apps/accounts/serializers.py`, `views.py` y `urls.py`: implementar `RegisterSerializer` y `POST /api/v1/auth/register/` con validación de contraseña y retorno inmediato de `token` + `user`.
   - En `frontend/src/services/authService.js`, `stores/auth.js`, `views/RegisterView.vue` y `views/LoginView.vue`: conectar el flujo de registro y navegación entre `/login`, `/register` y `/`.
