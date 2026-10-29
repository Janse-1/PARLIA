# TASKS: Plan Atómico de Ejecución y Hoja de Ruta

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)
**Institución:** Universidad de La Guajira - Facultad de Ingeniería (Sede Maicao)
**Estado Inicial:** Entorno virtual activo (`venv`), cero dependencias instaladas, repositorio en blanco.
**Regla de Oro:** Ejecutar una subtarea a la vez. No avanzar a la siguiente sin verificar su funcionamiento y marcar `[x]`.

---

## 📚 Módulos Oficiales del Laboratorio
1. **Módulo 1:** Fundamentos de la Inteligencia Artificial Generativa
2. **Módulo 2:** Ingeniería de Prompts
3. **Módulo 3:** Verificaciones
4. **Módulo 4:** Ética, Privacidad e Integridad Académica
5. **Módulo 5:** Aplicación en investigación, redacción
6. **Módulo 6:** Actividades finales

---

## Fase 1: Inicialización del Entorno, Configuración Base y Conexiones

**Objetivo:** Instalar dependencias esenciales, configurar la base de datos MySQL y dejar corriendo los servidores de desarrollo de Vue 3 y Django.

- [ ] **T1.1** Instalación de dependencias del Backend:
  - Verificar versión de Python (`python --version` $\ge$ 3.12).
  - Instalar dependencias base en el `venv`: `django`, `djangorestframework`, `django-cors-headers`, `mysqlclient`, `python-dotenv`.
  - Generar el archivo inicial `backend/requirements.txt` con las versiones fijadas.
- [ ] **T1.2** Inicialización del proyecto Django:
  - Crear la estructura del backend: `django-admin startproject config backend`.
  - Crear las aplicaciones modulares: `apps/accounts`, `apps/learning`, `apps/activities`, `apps/progress`.
  - Configurar `backend/.gitignore` asegurando la exclusión de `.env`, `__pycache__/` y archivos locales.
  - Crear `backend/.env.example` y el archivo `backend/.env` local.
- [ ] **T1.3** Configuración de Base de Datos y Settings:
  - Crear la base de datos en MySQL: `CREATE DATABASE parlia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`.
  - Configurar `backend/config/settings.py` para enlazar variables de entorno, aplicaciones locales, DRF y CORS.
  - Verificar conexión a MySQL ejecutando las migraciones base de Django (`python manage.py migrate`).
- [ ] **T1.4** Inicialización del Frontend con Vite:
  - Crear proyecto Vue 3 con Vite: `npm create vite@latest frontend -- --template vue`.
  - Acceder a `frontend/` e instalar dependencias del cliente: `npm install vue-router pinia axios animejs`.
  - Crear `frontend/.env.example` y `frontend/.env` con `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
  - Configurar la estructura de carpetas (`components/`, `views/`, `stores/`, `router/`, `services/`, `styles/`).
- [ ] **T1.5** *Exit Criteria Día 1:* Ambos servidores arrancan sin advertencias (`python manage.py runserver` en `localhost:8000` y `npm run dev` en `localhost:5173`).

---

## Fase 2: Modelado de Datos, Migraciones y Panel de Administración

**Objetivo:** Implementar los modelos relacionales en Django, aplicar restricciones de unicidad y configurar el panel de Django Admin para poblar los 6 módulos.

- [ ] **T2.1** Modelo de Usuario (`apps/accounts`):
  - Extender `AbstractUser` para crear el modelo `User` con campos `email` (único), `program` (Sistemas, Industrial, Mecánica, Civil, Otro) y nombre completo.
  - Registrar el modelo en `AUTH_USER_MODEL = 'accounts.User'`.
- [ ] **T2.2** Modelos de Aprendizaje (`apps/learning`):
  - Implementar `Module` (`title`, `slug`, `description`, `order`, `is_published`).
  - Implementar `Lesson` (`module`, `title`, `slug`, `content`, `estimated_minutes`, `order`, `is_published`) con restricción `UNIQUE (module_id, order)`.
  - Implementar `MediaAsset` (`lesson`, `title`, `asset_type`, `url`, `description`).
- [ ] **T2.3** Modelos de Actividades (`apps/activities`):
  - Implementar `Activity` (`lesson`, `title`, `description`, `activity_type`) con relación `OneToOne` con `Lesson`.
  - Implementar `Question` (`activity`, `prompt_text`, `options_json`, `explanation`, `order`).
  - Implementar `ActivityAttempt` (`user`, `activity`, `selected_option`, `reflection_text`, `is_correct`, `submitted_at`).
- [ ] **T2.4** Modelo de Progreso (`apps/progress`):
  - Implementar `LearningProgress` (`user`, `lesson`, `status`, `started_at`, `completed_at`, `updated_at`).
  - Definir la restricción obligatoria `UniqueConstraint(fields=['user', 'lesson'], name='unique_user_lesson_progress')`.
- [ ] **T2.5** Migraciones y Django Admin:
  - Generar y aplicar migraciones: `python manage.py makemigrations` y `python manage.py migrate`.
  - Registrar todos los modelos en los archivos `admin.py` correspondientes con filtros de búsqueda y visualización ordenada.
  - Crear superusuario: `python manage.py createsuperuser`.
  - Cargar desde el admin el esqueleto de los **6 módulos oficiales de PARLIA**.
- [ ] **T2.6** *Exit Criteria Día 2:* Base de datos estructurada en MySQL con sus tablas y llaves foráneas. Los 6 módulos creados y visibles en Django Admin.

---

## Fase 3: Desarrollo de la API REST (`/api/v1/`)
**Objetivo:** Construir y probar endpoints de autenticación, lectura de contenidos, actividades y registro de progreso sin brechas de seguridad (IDOR).

- [ ] **T3.1** Endpoints de Autenticación (`apps/accounts`):
  - Crear Serializers para login y datos de usuario.
  - Implementar vistas para `/api/v1/auth/login/`, `/api/v1/auth/logout/` y `/api/v1/me/`.
  - Probar autenticación por tokens o sesiones verificando el retorno seguro de datos.
- [ ] **T3.2** Endpoints de Contenido Pedagógico (`apps/learning`):
  - Crear `ModuleSerializer` y `LessonSerializer`.
  - Implementar endpoint `/api/v1/modules/` (listado ordenado de módulos publicados).
  - Implementar endpoint `/api/v1/modules/{id}/` (módulo con lista de lecciones).
  - Implementar endpoint `/api/v1/lessons/{id}/` (contenido completo de la lección y recursos multimedia).
- [ ] **T3.3** Endpoints de Progreso (`apps/progress`):
  - Crear `ProgressSerializer`.
  - Implementar endpoint `GET /api/v1/progress/me/` que extraiga `request.user` y devuelva el estado de todas las lecciones del estudiante.
  - Implementar endpoint `POST/PATCH /api/v1/progress/` para actualizar estado (`in_progress`, `completed`) usando `update_or_create` sin permitir manipulación de IDs externos.
- [ ] **T3.4** Endpoints de Actividades (`apps/activities`):
  - Implementar `GET /api/v1/activities/{id}/` para servir preguntas formativas sin revelar la respuesta correcta con antelación.
  - Implementar `POST /api/v1/activities/{id}/attempts/` para registrar intentos y devolver la explicación formativa.
- [ ] **T3.5** *Exit Criteria Día 3:* Todos los endpoints probados y respondiendo con formato estandarizado JSON (`status`, `data`, `message`). Cero vulnerabilidades IDOR.

---

## Fase 4: Frontend Base - Layout, Navegación y Vistas de Estudio

**Objetivo:** Maquetar la estructura visual de PARLIA en Vue 3 con tokens de Uniguajira, Sidebar plegable, Topbar fija y vista de lectura de lecciones.

- [ ] **T4.1** Sistema de Estilos y Tokens de Diseño:
  - Crear `frontend/src/styles/variables.css` con la paleta de Uniguajira (Ocre `#C2822B`, Aguamarina `#2A9D8F`, Flamenco `#E76F51`, Neutros `#F8F9FA`, `#1F2937`).
  - Configurar tipografía del sistema (`Inter`), estilos base y reseteo CSS.
- [ ] **T4.2** Componente Topbar Superior:
  - Maquetar la barra fija superior (`height: 64px`) con botón toggle `[≡]`, logo de PARLIA e íconos: `Videos`, `Noticias`, `Progreso` y `Perfil`.
  - Configurar enlaces y estados reactivos.
- [ ] **T4.3** Componente Sidebar Colapsable:
  - Crear el menú lateral con transición fluida entre estado expandido (`260px`) y colapsado (`72px` o drawer en móvil).
  - Integrar las secciones requeridas:
    - Desplegable de Carreras (Sistemas, Industrial, Mecánica, Civil, etc.).
    - Vista informativa de **Imágenes** (con aviso de que no afecta el progreso formal).
    - Vista informativa de **Redacción** (con aviso de que no afecta el progreso formal).
    - Biblioteca de **Prompts** con tarjetas limpias y botón de copiado rápido.
- [ ] **T4.4** Enrutamiento y Vistas de Contenido:
  - Configurar Vue Router (`router/index.js`) con las rutas principales: `/`, `/login`, `/modules`, `/modules/:id`, `/lessons/:id`, `/progress`, `/videos`, `/news`, `/profile`.
  - Construir la vista de Módulos (`ModulesView.vue`) mostrando las tarjetas de los 6 ejes pedagógicos.
  - Construir el Visor de Lección (`LessonDetailView.vue`) con lectura por bloques, navegación anterior/siguiente y llamada a actividades.
- [ ] **T4.5** *Exit Criteria Día 4:* Navegación fluida entre pantallas. El Sidebar se pliega y despliega correctamente. Las vistas de Imágenes, Redacción y Prompts son accesibles y no alteran métricas.

---

## Fase 5: Integración Cliente-Servidor, Estado Global y Progreso

**Objetivo:** Conectar el frontend con la API de Django usando Pinia y Axios para autenticación y guardado persistente del progreso.

- [ ] **T5.1** Configuración de Servicios y Cliente HTTP:
  - Crear `frontend/src/services/api.js` con la instancia configurada de Axios y manejo de encabezados de autorización.
  - Implementar servicios modulares: `authService.js`, `learningService.js`, `progressService.js`, `activityService.js`.
- [ ] **T5.2** Stores con Pinia:
  - Implementar `stores/auth.js` (estado del usuario, tokens/cookies, login, logout).
  - Implementar `stores/progress.js` (resumen de lecciones completadas, cálculo de porcentajes y sincronización con el servidor).
- [ ] **T5.3** Flujo de Autenticación Completo:
  - Conectar formulario de `LoginView.vue` con `/api/v1/auth/login/`.
  - Proteger rutas privadas mediante Navigation Guards en Vue Router (`beforeEach`).
- [ ] **T5.4** Sincronización del Avance del Estudiante:
  - Al abrir una lección, emitir evento para registrar estado `in_progress`.
  - Al terminar la lectura o actividad, permitir al estudiante marcar explícitamente `completed`.
  - Actualizar el store de Pinia y persistir el cambio en MySQL.
- [ ] **T5.5** *Exit Criteria Día 5:* Un estudiante inicia sesión, completa una lección, cierra sesión y al volver a entrar su progreso se mantiene intacto sin duplicados.

---

## Fase 6: "La Expedición del Guerrero a la Montaña" y Actividades Formativas

**Objetivo:** Desarrollar el mapa interactivo de progreso con SVG animado mediante Anime.js y habilitar los ejercicios formativos de las lecciones.

- [ ] **T6.1** Trazado SVG del Sendero del Guerrero:
  - Diseñar el vector SVG del camino serpenteante en `frontend/src/views/ProgressView.vue` conectando las 6 estaciones hacia la montaña.
  - Diferenciar visualmente los tramos recorridos (Aguamarina `#2A9D8F`) de los pendientes (gris `#D1D5DB`).
  - Representar los 6 módulos como campamentos con banderas ondeando en Coral `#E76F51` al ser completados.
- [ ] **T6.2** Animación con Anime.js:
  - Implementar la animación del trazado del camino (`strokeDashoffset`).
  - Animar el desplazamiento del avatar del guerrero hacia la estación correspondiente al progreso actual del estudiante utilizando `anime.path()`.
  - Condicionar la ejecución de animaciones a la directiva de accesibilidad `@media (prefers-reduced-motion: reduce)`.
- [ ] **T6.3** Componente de Actividades Formativas:
  - Construir el componente de preguntas en `LessonDetailView.vue` para selección múltiple y reflexión.
  - Mostrar explicaciones pedagógicas inmediatas tras responder, enfatizando el aprendizaje reflexivo y eliminando mensajes de castigo o penalización.
  - Registrar el intento formativo en la API al concluir.
- [ ] **T6.4** *Exit Criteria Día 6:* El mapa del guerrero se anima y ubica al personaje en la posición real según los datos de MySQL. Las actividades formativas funcionan y retroalimentan al usuario.

---

## Fase 7: Pruebas de Calidad, Auditoría de Seguridad y Puesta a Punto del Piloto

**Objetivo:** Auditar la plataforma en escritorio y móvil, verificar medidas de seguridad y dejar el laboratorio listo para demostración.

- [ ] **T7.1** Auditoría de Calidad de Datos y Seguridad:
  - Comprobar que no existen accesos no autorizados a datos de otros estudiantes (test de IDOR en `/api/v1/progress/`).
  - Confirmar que contraseñas no se exponen en logs y que `.env` está fuera del repositorio.
  - Verificar que `DEBUG=False` opera correctamente con `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS` configurados.
- [ ] **T7.2** Pruebas de Usabilidad y Responsividad:
  - Validar navegación y visualización en pantallas móviles (drawer lateral, mapa vertical adaptado, legibilidad de textos).
  - Verificar que no existan muros de texto excesivos y que el espacio en blanco (*whitespace*) sea generoso.
- [ ] **T7.3** Generación de Respaldo de Base de Datos:
  - Ejecutar volcado de prueba de MySQL (`mysqldump`) para asegurar que la información y el progreso pueden respaldarse y restaurarse sin pérdidas.
- [ ] **T7.4** Documentación y Cierre de Bitácoras:
  - Actualizar `docs/memory.md` con el estado final de la implementación.
  - Registrar las decisiones de arquitectura definitivas en `docs/decisions.md`.
- [ ] **T7.5** *Exit Criteria Día 7:* PARLIA funcional de punta a punta, con sus 6 módulos navegables, autenticación protegida, mapa del guerrero interactivo y datos persistidos en MySQL.
```

---

### Resumen del archivo generado
* **Plan secuencial de 7 días:** Estructurado desde el entorno inicial en blanco hasta el piloto funcional.
* **Integración de los 6 módulos oficiales:** Fundamentos, Prompts, Verificaciones, Ética e Integridad, Aplicación en investigación/redacción y Actividades finales.
* **Componentes clave cubiertos:** Sidebar colapsable (Carreras, Imágenes, Redacción, Prompts), Topbar (Videos, Noticias, Progreso, Perfil) y el mapa interactivo del guerrero hacia la montaña con Anime.js.
* **Criterios de salida explícitos:** Cada día cuenta con validación técnica antes de avanzar.