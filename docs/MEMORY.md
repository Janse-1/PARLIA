# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** ParLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-11-11  

---

## 1. Estado Actual de la Implementación
* **Estado Global:** **100% Completado** (Fases 1 a 8 cerradas y verificadas con `[x]` en `docs/TASKS.md`).
* **Backend (`d:\parlia\backend`):**
  - Django 5.2.18 LTS + Django REST Framework sobre MySQL 8.0.40 (`parlia_db`).
  - 4 aplicaciones de dominio operativas (`apps.accounts`, `apps.learning`, `apps.activities`, `apps.progress`).
  - Endpoints `/api/v1/` completos: `auth/login/`, `auth/register/`, `auth/logout/`, `me/`, `modules/`, `modules/{id}/`, `lessons/{id}/`, `progress/me/`, `progress/`, `activities/{id}/`, `activities/{id}/attempts/`.
  - Suite de pruebas automatizadas de seguridad anti-IDOR y registro self-service pasando al 100% (`manage.py test apps.accounts apps.progress --keepdb`).
* **Frontend (`d:\parlia\frontend`):**
  - Vue 3.5+ (`<script setup>`), Vite 8, Vue Router 4, Pinia 2, Axios y Anime.js 3.2.
  - **Portal de Bienvenida (`/` - `HomeView.vue`):** Video de fondo local (`gemini_generated_video_0609d70b.mp4`), animación interactiva de scroll a 60fps sobre `para_animar.jpeg` con revelación por zonas de luz y trazos de Anime.js, secciones con identidad propia de ParLIA (`#synapse`, `#pillars`, `#methodology`, `#audit`, `#identity`) y aislamiento total de módulos/carreras antes de iniciar sesión.
  - **Sistema de Temas e Idioma (`stores/theme.js` y `stores/i18n.js`):** Cambio instantáneo entre Modo Claro (`fondo_claro.jpeg`) y Modo Oscuro (`fondo_oscuro.jpeg`) con persistencia en `localStorage`, más selector global `ES | EN` en `Topbar.vue` y `Sidebar.vue`.
  - **Dashboard Ejecutivo de Progreso (`ProgressView.vue`):** Stepper interactivo de los 6 ejes oficiales, contadores numéricos, barras de calibración y anillos radiales de competencias técnicas animados con Anime.js.
* **Respaldo de Base de Datos (`d:\parlia\backups\parlia_db_backup.sql`):**
  - Generado y verificado mediante `mysqldump` (`39,789 bytes`, codificación `utf8mb4`).

---

## 2. Comandos de Ejecución Rápida
* **Backend:** `d:\parlia\.venv\Scripts\python.exe d:\parlia\backend\manage.py runserver`
* **Frontend:** `npm --prefix d:\parlia\frontend run dev`
* **Tests Backend:** `d:\parlia\.venv\Scripts\python.exe d:\parlia\backend\manage.py test --keepdb`
