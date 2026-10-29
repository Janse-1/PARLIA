# MEMORY: Estado Vivo del Sistema y Bitácora Técnica

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Última actualización:** 2026-10-28  

---

## 1. Estado Actual de la Implementación
* **Fase Activa:** Fase 1 (Inicialización del Entorno)
* **Subtareas Completadas:**
  - T1.1 (Instalación de dependencias del Backend)
  - T1.2 (Inicialización del proyecto Django y apps modulares)
  - T1.3 (Configuración de Base de Datos MySQL y Settings)
* **Subtarea Siguiente:** T1.4 (Inicialización del Frontend con Vite)

---

## 2. Configuración y Entorno de Ejecución
* **Python Virtualenv:** `.venv` funcional con Python 3.12.5.
* **Dependencias Backend (`backend/requirements.txt`):**
  - `Django==5.2.18` (LTS compatible con MySQL 8.0.40)
  - `djangorestframework==3.18.3`
  - `django-cors-headers==4.9.0`
  - `mysqlclient==2.3.0`
  - `python-dotenv==1.2.4`
* **Base de Datos MySQL:**
  - Base de datos `parlia_db` creada con `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci` en MySQL 8.0.40 (`127.0.0.1:3306`).
  - `backend/config/settings.py` enlazado a `.env`, con `rest_framework`, `corsheaders` y las 4 apps (`apps.accounts`, `apps.learning`, `apps.activities`, `apps.progress`) registradas.
  - Migraciones iniciales de Django aplicadas exitosamente en MySQL.

---

## 3. Próximos Pasos Inmediatos
1. Ejecutar **T1.4**:
   - Crear proyecto Vue 3 con Vite en `frontend/`.
   - Instalar dependencias del cliente: `vue-router`, `pinia`, `axios`, `animejs`.
   - Configurar `frontend/.env.example` y `frontend/.env` (`VITE_API_BASE_URL=http://localhost:8000/api/v1`).
   - Crear la estructura de directorios en `frontend/src/` (`assets/`, `components/`, `layouts/`, `router/`, `services/`, `stores/`, `styles/`, `views/`).
