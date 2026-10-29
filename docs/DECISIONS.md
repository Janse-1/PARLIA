# DECISIONS (ADR): Registro de Decisiones de Arquitectura y Técnicas

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  

---

## ADR-001: Fijación de versión de Django 5.2 LTS para compatibilidad con MySQL 8.0.40
* **Fecha:** 2026-10-28
* **Estado:** Aceptada
* **Contexto:** Al ejecutar `pip install django` sin restricción superior en el entorno virtual, se instaló inicialmente `Django 6.1.2`, la cual requiere estrictamente MySQL 8.4 o superior. El entorno de desarrollo local cuenta con **MySQL 8.0.40** y la documentación de arquitectura (`ARQUITECTURE.md` y `data_dictionary.md`) especifica el uso de Django 5.1+ sobre MySQL 8.0+.
* **Alternativas descartadas:**
  1. Actualizar el servidor MySQL local a 8.4+ (innecesario e invasivo para el entorno local del desarrollador).
  2. Omitir validaciones de versión de base de datos mediante monkey-patching (riesgo de incompatibilidad de SQL).
* **Decisión:** Fijar `Django==5.2.18` (rama 5.2 LTS) dentro de `backend/requirements.txt`.
* **Consecuencias:** Compatibilidad nativa y estable al 100% con MySQL 8.0.40 (`utf8mb4`), soporte LTS y alineación exacta con la arquitectura documentada.

---

## ADR-002: Recreación del entorno virtual `.venv` con ejecutable estándar de Python 3.12
* **Fecha:** 2026-10-28
* **Estado:** Aceptada
* **Contexto:** El entorno `.venv` inicial apuntaba al alias de ejecución de Microsoft Store (`WindowsApps\PythonSoftwareFoundation.Python.3.12...`), lo que provocaba un bloqueo de permisos en Windows (`Unable to create process`).
* **Decisión:** Recrear `.venv` utilizando la instalación estándar del sistema en `C:\Users\chapl\AppData\Local\Programs\Python\Python312\python.exe` (Python 3.12.5).
* **Consecuencias:** Ejecución fluida y sin bloqueos de `python`, `pip` y `django-admin` dentro del entorno virtual.

