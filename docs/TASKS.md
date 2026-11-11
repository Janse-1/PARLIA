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

- [x] **T1.1** Instalación de dependencias del Backend:
  - Verificar versión de Python (`python --version` $\ge$ 3.12).
  - Instalar dependencias base en el `venv`: `django`, `djangorestframework`, `django-cors-headers`, `mysqlclient`, `python-dotenv`.
  - Generar el archivo inicial `backend/requirements.txt` con las versiones fijadas.
- [x] **T1.2** Inicialización del proyecto Django:
  - Crear la estructura del backend: `django-admin startproject config backend`.
  - Crear las aplicaciones modulares: `apps/accounts`, `apps/learning`, `apps/activities`, `apps/progress`.
  - Configurar `backend/.gitignore` asegurando la exclusión de `.env`, `__pycache__/` y archivos locales.
  - Crear `backend/.env.example` y el archivo `backend/.env` local.
- [x] **T1.3** Configuración de Base de Datos y Settings:
  - Crear la base de datos en MySQL: `CREATE DATABASE parlia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`.
  - Configurar `backend/config/settings.py` para enlazar variables de entorno, aplicaciones locales, DRF y CORS.
  - Verificar conexión a MySQL ejecutando las migraciones base de Django (`python manage.py migrate`).
- [/] **T1.4** Inicialización del Frontend con Vite:
  - Crear proyecto Vue 3 con Vite: `npm create vite@latest frontend -- --template vue`.
  - Acceder a `frontend/` e instalar dependencias del cliente: `npm install vue-router pinia axios animejs`.
  - Crear `frontend/.env.example` y `frontend/.env` con `VITE_API_BASE_URL=http://localhost:8000/api/v1`.
  - Configurar la estructura de carpetas (`components/`, `views/`, `stores/`, `router/`, `services/`, `styles/`).
- [ ] **T1.5** *Exit Criteria Día 1:* Ambos servidores arrancan sin advertencias (`python manage.py runserver` en `localhost:8000` y `npm run dev` en `localhost:5173`).

---

## Fase 2: Modelado de Datos, Migraciones y Panel de Administración

**Objetivo:** Implementar los modelos relacionales en Django, aplicar restricciones de unicidad y configurar el panel de Django Admin para poblar los 6 módulos.

- [x] **T2.1** Modelo de Usuario (`apps/accounts`):
  - Extender `AbstractUser` para crear el modelo `User` con campos `email` (único), `program` (Sistemas, Industrial, Mecánica, Civil, Ambiental, Energias, Otro) y nombre completo.
  - Registrar el modelo en `AUTH_USER_MODEL = 'accounts.User'`.
- [x] **T2.2** Modelos de Aprendizaje (`apps/learning`):
  - Implementar `Module` (`title`, `slug`, `description`, `order`, `is_published`).
  - Implementar `Lesson` (`module`, `title`, `slug`, `content`, `estimated_minutes`, `order`, `is_published`) con restricción `UNIQUE (module_id, order)`.
  - Implementar `MediaAsset` (`lesson`, `title`, `asset_type`, `url`, `description`).
- [x] **T2.3** Modelos de Actividades (`apps/activities`):
  - Implementar `Activity` (`lesson`, `title`, `description`, `activity_type`) con relación `OneToOne` con `Lesson`.
  - Implementar `Question` (`activity`, `prompt_text`, `options_json`, `explanation`, `order`).
  - Implementar `ActivityAttempt` (`user`, `activity`, `selected_option`, `reflection_text`, `is_correct`, `submitted_at`).
- [x] **T2.4** Modelo de Progreso (`apps/progress`):
  - Implementar `LearningProgress` (`user`, `lesson`, `status`, `started_at`, `completed_at`, `updated_at`).
  - Definir la restricción obligatoria `UniqueConstraint(fields=['user', 'lesson'], name='unique_user_lesson_progress')`.
- [x] **T2.5** Migraciones y Django Admin:
  - Generar y aplicar migraciones: `python manage.py makemigrations` y `python manage.py migrate`.
  - Registrar todos los modelos en los archivos `admin.py` correspondientes con filtros de búsqueda y visualización ordenada.
  - Crear superusuario: `python manage.py createsuperuser`.
  - Cargar desde el admin el esqueleto de los **6 módulos oficiales de PARLIA**.
- [x] **T2.6** *Exit Criteria Día 2:* Base de datos estructurada en MySQL con sus tablas y llaves foráneas. Los 6 módulos creados y visibles en Django Admin.

---

## Fase 3: Desarrollo de la API REST (`/api/v1/`)
**Objetivo:** Construir y probar endpoints de autenticación, lectura de contenidos, actividades y registro de progreso sin brechas de seguridad (IDOR).

- [x] **T3.1** Endpoints de Autenticación (`apps/accounts`):
  - Crear Serializers para login y datos de usuario.
  - Implementar vistas para `/api/v1/auth/login/`, `/api/v1/auth/logout/` y `/api/v1/me/`.
  - Probar autenticación por tokens o sesiones verificando el retorno seguro de datos.
- [x] **T3.2** Endpoints de Contenido Pedagógico (`apps/learning`):
  - Crear `ModuleSerializer` y `LessonSerializer`.
  - Implementar endpoint `/api/v1/modules/` (listado ordenado de módulos publicados).
  - Implementar endpoint `/api/v1/modules/{id}/` (módulo con lista de lecciones).
  - Implementar endpoint `/api/v1/lessons/{id}/` (contenido completo de la lección y recursos multimedia).
- [x] **T3.3** Endpoints de Progreso (`apps/progress`):
  - Crear `ProgressSerializer`.
  - Implementar endpoint `GET /api/v1/progress/me/` que extraiga `request.user` y devuelva el estado de todas las lecciones del estudiante.
  - Implementar endpoint `POST/PATCH /api/v1/progress/` para actualizar estado (`in_progress`, `completed`) usando `update_or_create` sin permitir manipulación de IDs externos.
- [x] **T3.4** Endpoints de Actividades (`apps/activities`):
  - Implementar `GET /api/v1/activities/{id}/` para servir preguntas formativas sin revelar la respuesta correcta con antelación.
  - Implementar `POST /api/v1/activities/{id}/attempts/` para registrar intentos y devolver la explicación formativa.
- [x] **T3.5** *Exit Criteria Día 3:* Todos los endpoints probados y respondiendo con formato estandarizado JSON (`status`, `data`, `message`). Cero vulnerabilidades IDOR.

---

## Fase 4: Frontend Base - Layout, Navegación y Vistas de Estudio

**Objetivo:** Maquetar la estructura visual de PARLIA en Vue 3 con tokens de Uniguajira, Sidebar plegable, Topbar fija y vista de lectura de lecciones.

- [x] **T4.1** Sistema de Estilos y Tokens de Diseño:
  - Crear `frontend/src/styles/variables.css` con la paleta de Uniguajira (Ocre `#C2822B`, Aguamarina `#2A9D8F`, Flamenco `#E76F51`, Neutros `#F8F9FA`, `#1F2937`).
  - Configurar tipografía del sistema (`Inter`), estilos base y reseteo CSS.
- [x] **T4.2** Componente Topbar Superior:
  - Maquetar la barra fija superior (`height: 64px`) con botón toggle `[≡]`, logo de PARLIA e íconos: `Videos`, `Noticias`, `Progreso` y `Perfil`.
  - Configurar enlaces y estados reactivos.
- [x] **T4.3** Componente Sidebar Colapsable:
  - Crear el menú lateral con transición fluida entre estado expandido (`260px`) y colapsado (`72px` o drawer en móvil).
  - Integrar las secciones requeridas:
    - Desplegable de Carreras (Sistemas, Industrial, Mecánica, Civil, etc.).
    - Vista informativa de **Imágenes** (con aviso de que no afecta el progreso formal).
    - Vista informativa de **Redacción** (con aviso de que no afecta el progreso formal).
    - Biblioteca de **Prompts** con tarjetas limpias y botón de copiado rápido.
- [x] **T4.4** Enrutamiento y Vistas de Contenido:
  - Configurar Vue Router (`router/index.js`) con las rutas principales: `/`, `/login`, `/modules`, `/modules/:id`, `/lessons/:id`, `/progress`, `/videos`, `/news`, `/profile`.
  - Construir la vista de Módulos (`ModulesView.vue`) mostrando las tarjetas de los 6 ejes pedagógicos.
  - Construir el Visor de Lección (`LessonDetailView.vue`) con lectura por bloques, navegación anterior/siguiente y llamada a actividades.
- [x] **T4.5** *Exit Criteria Día 4:* Navegación fluida entre pantallas. El Sidebar se pliega y despliega correctamente. Las vistas de Imágenes, Redacción y Prompts son accesibles y no alteran métricas.

---

## Fase 5: Integración Cliente-Servidor, Estado Global y Progreso

**Objetivo:** Conectar el frontend con la API de Django usando Pinia y Axios para autenticación y guardado persistente del progreso.

- [x] **T5.1** Configuración de Servicios y Cliente HTTP:
  - Crear `frontend/src/services/api.js` con la instancia configurada de Axios y manejo de encabezados de autorización.
  - Implementar servicios modulares: `authService.js`, `learningService.js`, `progressService.js`, `activityService.js`.
- [x] **T5.2** Stores con Pinia:
  - Implementar `stores/auth.js` (estado del usuario, tokens/cookies, login, logout).
  - Implementar `stores/progress.js` (resumen de lecciones completadas, cálculo de porcentajes y sincronización con el servidor).
- [x] **T5.3** Flujo de Autenticación Completo:
  - Conectar formulario de `LoginView.vue` con `/api/v1/auth/login/`.
  - Proteger rutas privadas mediante Navigation Guards en Vue Router (`beforeEach`).
- [x] **T5.4** Sincronización del Avance del Estudiante:
  - Al abrir una lección, emitir evento para registrar estado `in_progress`.
  - Al terminar la lectura o actividad, permitir al estudiante marcar explícitamente `completed`.
  - Actualizar el store de Pinia y persistir el cambio en MySQL.
- [x] **T5.5** *Exit Criteria Día 5:* Un estudiante inicia sesión, completa una lección, cierra sesión y al volver a entrar su progreso se mantiene intacto sin duplicados.

---

## Fase 6: "La Expedición del Guerrero a la Montaña" y Actividades Formativas

**Objetivo:** Desarrollar el mapa interactivo de progreso con SVG animado mediante Anime.js y habilitar los ejercicios formativos de las lecciones.

- [x] **T6.1** Trazado SVG del Sendero del Guerrero:
  - Diseñar el vector SVG del camino serpenteante en `frontend/src/views/ProgressView.vue` conectando las 6 estaciones hacia la montaña.
  - Diferenciar visualmente los tramos recorridos (Aguamarina `#2A9D8F`) de los pendientes (gris `#D1D5DB`).
  - Representar los 6 módulos como campamentos con banderas ondeando en Coral `#E76F51` al ser completados.
- [x] **T6.2** Animación con Anime.js:
  - Implementar la animación del trazado del camino (`strokeDashoffset`).
  - Animar el desplazamiento del avatar del guerrero hacia la estación correspondiente al progreso actual del estudiante utilizando `anime.path()`.
  - Condicionar la ejecución de animaciones a la directiva de accesibilidad `@media (prefers-reduced-motion: reduce)`.
- [x] **T6.3** Componente de Actividades Formativas:
  - Construir el componente de preguntas en `LessonDetailView.vue` para selección múltiple y reflexión.
  - Mostrar explicaciones pedagógicas inmediatas tras responder, enfatizando el aprendizaje reflexivo y eliminando mensajes de castigo o penalización.
  - Registrar el intento formativo en la API al concluir.
- [x] **T6.4** *Exit Criteria Día 6:* El mapa del guerrero se anima y ubica al personaje en la posición real según los datos de MySQL. Las actividades formativas funcionan y retroalimentan al usuario.

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
```
## 🚀 Fase 8: Rediseño Visual, Portal de Bienvenida (CRM-Hero), Temas y Experiencia Refinada

**Objetivo:** Transformar la experiencia visual eliminando la sobrecarga y el exceso de bordes redondeados, incorporando una Landing/Portal ejecutivo con video de fondo cinemático optimizado, animación SVG con el isotipo oficial ParLIA, autoservicio de registro de usuarios, cambio de tema claro/oscuro nativo, selector de idioma y un rediseño sobrio e interactivo de la vista de progreso.

### 8.1. Arquitectura de Rutas y Portal de Bienvenida (No forzar Login al entrar)
- [/] **T8.1.1** Reconfiguración de rutas en `router/index.js`:
  - Definir la ruta raíz `/` como el **Portal de Bienvenida / Dashboard General de ParLIA** accesible públicamente (sin redirigir al login por defecto).
  - Mover el formulario de inicio de sesión a `/login` y crear la ruta `/register` para nuevos estudiantes.
  - Actualizar Navigation Guards: permitir navegación exploratoria pública al portal general y exigir autenticación únicamente al ingresar al visor detallado de lecciones o al guardar progreso personal.
- [/] **T8.1.2** Maquetación de la Vista Principal (`HomeView.vue` - Estilo CRM Ejecutivo):
  - Crear la estructura Hero de alto impacto: video de fondo en bucle sutil con overlay de degradado profesional (`backdrop-blur` ligero, sin oscurecer ni quemar los colores).
  - Contenedor interactivo sobre el video con el isotipo SVG oficial de ParLIA animado mediante Anime.js (trazado de líneas Wayuu/tecnológicas y pulsos de conexión).
  - Título y propuesta de valor clara: *"ParLIA: Educación e Inteligencia Artificial"* con botones de acción rápida: `[Explorar Módulos]`, `[Registrarme]` e `[Iniciar Sesión]`.
  - Sección inferior tipo CRM Dashboard con métricas agregadas sobrias (6 módulos de ingeniería, estadísticas de cobertura, accesos rápidos a carreras y resumen visual del ecosistema sin saturación).

### 8.2. Registro de Nuevos Estudiantes (Self-Service)
- [ ] **T8.2.1** Endpoint de registro en el Backend (`apps/accounts`):
  - Implementar `RegisterSerializer` con validación de correo institucional (`@uniguajira.edu.co` opcional o abierto con selección de carrera: Sistemas, Industrial, Mecánica, Civil, Otro).
  - Crear endpoint `POST /api/v1/auth/register/` con validación segura de contraseñas (Django password validators) y login automático inmediato tras registro exitoso.
- [ ] **T8.2.2** Vista de Registro en el Frontend (`RegisterView.vue`):
  - Formulario limpio, sin marcos sobrecargados: nombre, correo, programa académico, contraseña y confirmación.
  - Integración con Pinia `authStore.register()` y redirección inmediata al portal o a los módulos.

### 8.3. Rediseño del Sistema de Diseño (Menos Curvas, Más Elegancia y Tipografía Nítida)
- [ ] **T8.3.1** Depuración de Tokens de Estilo (`styles/variables.css`):
  - Reducir drásticamente los radios de borde en toda la aplicación: cambiar `border-radius: 9999px` / `24px` a bordes planos sutiles (`border-radius: 4px` o `6px` máximo).
  - Eliminar sombras pesadas tipo neumorfismo o flotaciones artificiales; adoptar bordes de precisión `1px solid var(--border-color)` con contraste controlado.
  - Ajustar la paleta a los tonos corporativos exactos de la imagen oficial de ParLIA: Azul Petróleo Oscuro (`#0C1E2F`), Naranja/Coral Vivo (`#FF5B26`), Ocre (`#F99D1C`), Cian Wayuu (`#20A4B8`) y Blanco Puro (`#FFFFFF`).
- [ ] **T8.3.2** Sistema de Modo Claro y Modo Oscuro (Dark / Light Theme):
  - Crear el switch de tema en el Topbar con persistencia en `localStorage` y detección automática de preferencia del sistema (`prefers-color-scheme`).
  - Definir las variables CSS para ambos temas:
    - *Modo Claro:* Fondo `#F8F9FA` / `#FFFFFF`, texto `#0C1E2F`, tarjetas con bordes `#E2E8F0`, logo con versión clara (`fondo_claro.jpeg`).
    - *Modo Oscuro:* Fondo profundo `#08131E` / `#0C1E2F`, texto `#F1F5F9`, bordes `#1E3A54`, logo con versión oscura (`fondo_oscuro.jpeg`).
  - Crear un store en Pinia (`stores/theme.js`) que administre la clase `.dark` en la etiqueta `<html>`.

### 8.4. Internacionalización / Selector de Idioma (i18n)
- [ ] **T8.4.1** Estructura base de traducción:
  - Crear módulo de textos o integrar `vue-i18n` básico con soporte para Español (ES) e Inglés (EN).
  - Añadir control selector de idioma en el Topbar (`ES | EN`) con guardado de preferencia en `localStorage`.
  - Traducir elementos de navegación global: Módulos, Videos, Noticias, Progreso, Perfil, Login, Registro, Buscar y etiquetas de estado.

### 8.5. Ajustes de Navegación, Logotipo Dinámico y Enlaces
- [ ] **T8.5.1** Logotipo Oficial Dinámico con Retorno al Inicio:
  - Configurar el logo de ParLIA en el Topbar y Sidebar como un enlace interactivo hacia `/` (`router-link to="/"`).
  - Hacer que la imagen del logo cambie automáticamente entre `fondo_claro.jpeg` y `fondo_oscuro.jpeg` dependiendo del tema activo (claro u oscuro).
  - Aplicar cursor pointer y micro-interacción sutil de escala al pasar el mouse.
- [ ] **T8.5.2** Limpieza y ergonomía del Topbar y Sidebar:
  - Mantener en el Topbar: Selector de Idioma (`ES/EN`), Switch de Tema (`☀️/🌙`), `[📺 Videos]`, `[📰 Noticias]`, `[🎯 Progreso]` y `[👤 Perfil]` (o botones de Login/Registro si no hay sesión activa).
  - Ajustar el Sidebar izquierdo para que sea plano, discreto y retráctil, sin curvas gruesas.

### 8.6. Rediseño del Módulo de Progreso (Reemplazo del diseño anterior de la montaña)
- [ ] **T8.6.1** Arquitectura de la Vista de Progreso (`ProgressView.vue`):
  - Descartar el estilo caricaturesco con conos; construir un **Dashboard Ejecutivo de Hitos y Maestría (Inspiración CRM / Timeline)**.
  - Estructurar el avance como una ruta tecnológica horizontal/vertical modular de alta precisión (Stepper interactivo con nodos de estado: completado, activo, bloqueado).
  - Cada hito muestra: nombre del módulo, porcentaje real, tiempo invertido y botón de acceso rápido.
- [ ] **T8.6.2** Animación refinada de Progreso con Anime.js:
  - Animar el llenado de barras de calibración y medidores numéricos (`0% -> XX%`) con curvas suaves al entrar a la vista.
  - Tarjeta de resumen de habilidades técnicas (Prompting, Auditoría, Ética, Código) con indicadores radiales limpios.

### 8.7. Validación, Rendimiento y Pruebas
- [ ] **T8.7.1** Optimización del Video de Fondo y Assets:
  - Verificar que el video de fondo se reproduzca en `autoplay`, `muted`, `loop`, `playsinline` con fallback de poster para bajo consumo de datos y móviles.
  - Asegurar carga diferida (*lazy loading*) y que las animaciones de Anime.js no superen el 2% de uso continuo de CPU.
- [ ] **T8.7.2** *Exit Criteria Fase 8:* Al ingresar a `localhost:5173` se presenta el portal ParLIA con video y SVG animados, navegación fluida, cambio instantáneo de tema e idioma, registro libre y progreso rediseñado sin bordes sobrecargados.
```

---

### Resumen de los cambios incorporados en la hoja de ruta
1. **Días 1 a 6 cerrados `[x]`:** Se refleja el avance técnico completado en la lógica, modelos, migraciones y endpoints.
2. **Fase 8 añadida:**
   * **Portal de entrada abierto (`/`):** La página principal no fuerza al login; ofrece una vista ejecutiva estilo CRM con video de fondo optimizado (siguiendo la inspiración del video hero) y animación SVG del imagotipo Wayuu/IA de ParLIA.
   * **Autoservicio de registro:** Nuevos usuarios pueden registrarse directamente con su carrera.
   * **Estética plana y profesional:** Eliminación de los bordes excesivamente redondeados y sombras pesadas, adoptando una interfaz nítida y minimalista.
   * **Modo Claro / Modo Oscuro:** Integración de los dos logos oficiales provistos (`fondo_claro.jpeg` y `fondo_oscuro.jpeg`) con paleta sincronizada.
   * **Selector de Idioma:** Control `ES / EN` en el Topbar con persistencia.
   * **Logo interactivo:** Clic en el logo redirige siempre al inicio.
   * **Rediseño del Progreso:** Sustitución de los conos y la montaña por un timeline interactivo y profesional tipo dashboard de maestría.