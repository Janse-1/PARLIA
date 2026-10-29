# ARCHITECTURE: Arquitectura del Sistema y Entorno Técnico

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Versión:** 1.0 (MVP)  
**Estado:** Definido / En Planificación  

---

## 1. Visión General del Sistema

PARLIA está concebido como una plataforma web educativa diseñada para que los estudiantes de ingeniería experimenten y desarrollen competencias en Inteligencia Artificial Generativa bajo un enfoque reflexivo y no punitivo. 

Para cumplir el objetivo de entrega funcional en una semana sin comprometer la seguridad ni la mantenibilidad, la arquitectura del sistema se implementa como un **Monolito Modular Desacoplado**:
* **Frontend:** Single Page Application (SPA) reactiva y ligera construida con Vue 3 y Vite.
* **Backend:** API REST desacoplada implementada con Django y Django REST Framework (DRF), estructurada en aplicaciones modulares por dominio de negocio.
* **Persistencia:** Base de datos relacional única (MySQL) para toda la información estructurada y progreso de usuario.
* **Multimedia:** Gestión mediante metadatos y enlaces seguros a recursos externos en esta fase.

```text
+------------------------------------------------------------------+
|                   Cliente / Estudiante                           |
|        (Navegador Web Escritorio / Móvil - HTTPS)                |
+------------------------------------------------------------------+
                                │
                                ▼
+------------------------------------------------------------------+
|               Capa de Presentación (Frontend)                    |
|  • Vue 3 (Composition API) + Vite                                |
|  • Vue Router (Rutas Públicas y Protegidas)                      |
|  • Pinia (Estado Global de Sesión y Progreso)                    |
|  • Axios / Fetch (Cliente HTTP)                                  |
|  • CSS Modular + Anime.js (Micro-interacciones sutiles)          |
+------------------------------------------------------------------+
                                │
                                │ HTTPS / JSON (API REST /api/v1/)
                                ▼
+------------------------------------------------------------------+
|               Capa de Lógica de Negocio (Backend)                |
|  • Python 3.12.10 / Django / Django REST Framework                 |
|  • Django Admin (Gestión de contenidos durante el MVP)           |
|                                                                  |
|  [apps/accounts]    Autenticación, usuarios y roles              |
|  [apps/learning]    Módulos (6) y lecciones                      |
|  [apps/activities]  Ejercicios prácticos, preguntas y respuestas |
|  [apps/progress]    Control de avance e integridad (sin dups)    |
+------------------------------------------------------------------+
                                │
                                │ Conexión ORM (mysqlclient)
                                ▼
+------------------------------------------------------------------+
|                 Capa de Datos (Persistencia)                     |
|  • MySQL (Motor InnoDB, Charset utf8mb4)                         |
|  • Transacciones ACID y restricciones únicas compuestas          |
+------------------------------------------------------------------+
```

---

## 2. Stack Tecnológico

### 2.1. Frontend
* **Core:** Vue 3.5+ con Composition API (`<script setup>`).
* **Tooling / Bundler:** Vite 5+.
* **Enrutamiento:** Vue Router 4 (modo HTML5 History).
* **Gestión de Estado:** Pinia 2+.
* **Cliente de Red:** Axios 1.7+ (interceptor para tokens/sesión y manejo unificado de errores).
* **Animaciones:** Anime.js 3.2+ (limitado a transformaciones de opacidad y desplazamiento ligero). https://animejs.com/
* **Estilos:** CSS3 nativo modularizado con variables CSS, enfocado en diseño fluido y cumplimiento de `prefers-reduced-motion`.

### 2.2. Backend
* **Lenguaje:** Python 3.12.10
* **Framework Web:** Django 5.1+.
* **Framework de API:** Django REST Framework (DRF) 3.15+.
* **Conector de BD:** `mysqlclient` 2.2+.
* **Manejo de CORS:** `django-cors-headers`.
* **Configuración y Secretos:** `python-dotenv`.

### 2.3. Base de Datos
* **Motor:** MySQL 8.0+.
* **Configuración:** Tablas bajo motor InnoDB, codificación de caracteres `utf8mb4` e intercalación `utf8mb4_unicode_ci`.

---

## 3. Estructura del Repositorio (Monorepo)

Se organiza el proyecto en un único repositorio con separación física absoluta de código fuente para frontend y backend, sin utilizar Docker durante la primera semana de desarrollo local.

```text
parlia/
├── frontend/                     # Aplicación cliente SPA
│   ├── public/                   # Recursos estáticos no compilados (favicon, logo)
│   ├── src/
│   │   ├── assets/               # Imágenes optimizadas y vectores
│   │   ├── components/           # Componentes UI reutilizables (Navbar, ProgressBar, Modal)
│   │   ├── layouts/              # Plantillas maestras (AuthLayout, MainLayout)
│   │   ├── router/               # Definición y guardias de navegación
│   │   ├── services/             # Módulos de conexión HTTP por endpoint
│   │   ├── stores/               # Stores reactivos de Pinia (auth.js, progress.js)
│   │   ├── styles/               # Variables de tema, reset y tipografía
│   │   ├── views/                # Vistas principales de página
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── ModulesView.vue
│   │   │   ├── LessonDetailView.vue
│   │   │   └── ProgressView.vue
│   │   ├── App.vue
│   │   └── main.js               # Punto de entrada de Vue
│   ├── .env.example              # Variables cliente (VITE_API_BASE_URL)
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # API REST Django
│   ├── config/                   # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                     # Módulos desacoplados de dominio
│   │   ├── accounts/             # Modelos de usuario, serializers, auth views
│   │   ├── learning/             # Módulos, lecciones, recursos multimedia
│   │   ├── activities/           # Actividades y preguntas de reflexión
│   │   └── progress/             # Persistencia del progreso de aprendizaje
│   ├── manage.py
│   ├── requirements.txt          # Dependencias Python fijadas
│   └── .env.example              # Plantilla de configuración local
│
├── docs/                         # Documentación viva del sistema
│   ├── prd.md
│   ├── rules.md
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── design.md
│   └── tasks.md
│
├── .gitignore
└── README.md
```

---

## 4. Diseño Modular del Backend (Django Apps)

El monolito se divide en cuatro sub-aplicaciones internas para garantizar que la lógica de negocio se mantenga desacoplada y fácilmente testeable:

1. **`apps.accounts`**:
   * Responsable de la gestión del ciclo de vida del usuario (`User`).
   * Proveedor de autenticación (Login, Logout, `/api/v1/me/`).
   * Aplicación de políticas de contraseñas mediante hashing seguro PBKDF2/Argon2.
2. **`apps.learning`**:
   * Modelado y exposición del contenido pedagógico estructurado (`Module`, `Lesson`, `MediaAsset`).
   * Catálogo de los 6 módulos educativos del laboratorio.
   * Filtros de consulta para asegurar que solo se sirvan lecciones activas/publicadas.
3. **`apps.activities`**:
   * Gestión de ejercicios breves (`Activity`, `Question`).
   * Almacenamiento opcional de intentos y respuestas formativas (`ActivityAttempt`).
   * Validación técnica de respuestas sin fines punitivos.
4. **`apps.progress`**:
   * Seguimiento granular del avance del estudiante (`LearningProgress`).
   * Regla de negocio crítica: restricción única compuesta (`user`, `lesson`).
   * Cálculo en tiempo real de porcentajes de completitud por módulo.

---

## 5. Diseño y Especificación de la API REST (`/api/v1/`)

Toda la comunicación cliente-servidor se canaliza a través de JSON sobre HTTPS, con prefijo unificado de versión.

### 5.1. Matriz de Endpoints

| Método | Endpoint | Acceso | Propósito |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login/` | Público | Autenticar credenciales y establecer sesión o devolver token |
| `POST` | `/api/v1/auth/logout/` | Autenticado | Invalidar sesión o revocar token |
| `GET` | `/api/v1/me/` | Autenticado | Obtener información del perfil del estudiante activo |
| `GET` | `/api/v1/modules/` | Autenticado | Listar los 6 módulos con metadatos y estado general |
| `GET` | `/api/v1/modules/{id}/` | Autenticado | Obtener detalle de un módulo con el listado de sus lecciones |
| `GET` | `/api/v1/lessons/{id}/` | Autenticado | Obtener el contenido pedagógico de una lección específica |
| `GET` | `/api/v1/progress/me/` | Autenticado | Obtener el resumen global y detallado del progreso del estudiante |
| `POST` / `PATCH` | `/api/v1/progress/` | Autenticado | Registrar o actualizar el estado de una lección (`in_progress`, `completed`) |
| `GET` | `/api/v1/activities/{id}/` | Autenticado | Obtener actividad y preguntas asociadas a una lección |
| `POST` | `/api/v1/activities/{id}/attempts/` | Autenticado | Registrar intento formativo voluntario |

### 5.2. Formato Estándar de Respuesta

* **Respuesta Exitosa (HTTP 200/201):**
  ```json
  {
    "status": "success",
    "data": { ... }
  }
  ```
* **Respuesta de Error (HTTP 400/401/403/404/500):**
  ```json
  {
    "status": "error",
    "code": "PERMISSION_DENIED",
    "message": "No tiene autorización para modificar este recurso.",
    "details": {}
  }
  ```

---

## 6. Seguridad y Protección de Datos

### 6.1. Prevención de IDOR (Insecure Direct Object References)
En ningún caso la API aceptará el `user_id` desde el cuerpo de la petición o como parámetro en la URL para consultar o registrar progreso. El backend extraerá siempre la identidad del estudiante directamente desde `request.user` tras validar la firma de autenticación.

### 6.2. Variables de Entorno y Secretos
* Todas las claves maestras (`DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) se consumen desde `.env`.
* `.env` se encuentra explícitamente listado en `.gitignore`.

### 6.3. CORS y Encabezados de Red
* `django-cors-headers` configurado con lista blanca estricta (`CORS_ALLOWED_ORIGINS`).
* Cookies con flags `HttpOnly`, `Secure` (en producción) y `SameSite='Lax'` para mitigar ataques XSS y CSRF.

---

## 7. Estrategia de Persistencia y Base de Datos

* **Motor Relacional:** MySQL con motor de almacenamiento InnoDB para garantizar integridad referencial y transacciones ACID.
* **Control de Concurrencia en Progreso:** La tabla `progress_learningprogress` implementa la restricción única `UNIQUE KEY (user_id, lesson_id)` a nivel de base de datos. Cualquier actualización posterior se ejecuta mediante `UPDATE` o `update_or_create()` en el ORM de Django, impidiendo inconsistencias de duplicación.
* **Política de Medios:** La tabla `learning_mediaasset` almacena cadenas de texto con URLs de proveedores externos y metadatos (tipo MIME, título alternativo, descripción). Cero persistencia binaria (`BLOB`) en la base de datos.

---

## 8. Ciclo de Despliegue y Hoja de Ruta de Infraestructura

Para cumplir la entrega en 7 días, el proyecto evoluciona en etapas claras:

```text
[ Etapa 1: MVP en 1 Semana (Desarrollo Local Directo) ]
  • Python venv + Node.js nativo en máquina de desarrollo
  • MySQL Server local
  • Sin Docker, sin Redis, sin Celery
         │
         ▼
[ Etapa 2: Piloto de Validación (Demostración Controlada) ]
  • Frontend compilado como estático (Vite Build)
  • Backend ejecutado en servidor de aplicaciones (Gunicorn/Uvicorn)
  • Instancia MySQL administrada con backups automáticos
  • Encriptación SSL/TLS activa (HTTPS obligatorio)
         │
         ▼
[ Etapa 3: Preparación para Producción Escalable ]
  • Dockerfile multi-stage para Frontend y Backend
  • Orquestación mediante Docker Compose / Kubernetes
  • Caché de lecciones mediante Redis
  • Almacenamiento de objetos S3 compatible (p. ej. Cloudflare R2)
  • Integración de monitoreo de errores y métricas (Sentry / Prometheus)
```