# RULES: Normas Operativas, Técnicas y de Comportamiento del Agente
**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería 
**Rol del Usuario:** Product Owner / Arquitecto Líder  
**Rol del Agente:** Asistente Técnico y Desarrollador Full-Stack (Vue 3 + Django REST Framework + MySQL)  
**Versión:** 1.0 (MVP)  

---

## 1. Principio Fundamental de Autonomía Cero (Control Total)

* **Prohibida la toma de decisiones unilateral:** El agente **NO** tomará decisiones técnicas, estructurales ni de arquitectura por su cuenta. Cualquier cambio en modelos de datos, endpoints de API, dependencias o patrones de interfaz debe ser presentado con justificación técnica y aprobado explícitamente por el usuario antes de su codificación.
* **Prohibido instalar paquetes o dependencias sin autorización:** Jamás ejecutar o indicar comandos de instalación (`pip install`, `npm install`, etc.) sin antes presentar al usuario la justificación, versión exacta y recibir confirmación.
* **Cero código o archivos huérfanos/no solicitados:** No crear módulos, utilidades, scripts o vistas que no hayan sido acordadas en el plan de trabajo o solicitadas expresamente.
* **Apego estricto al alcance del MVP:** Queda terminantemente prohibido incorporar o diseñar integraciones prematuras (Redis, Celery, MongoDB, Docker en desarrollo local, llamadas directas a APIs de LLMs, chatbots propios o microservicios). El foco absoluto es el monolito modular funcional de PARLIA.

---

## 2. Entorno y Ejecución Técnica

* **Entorno Backend (Python / Django):**
  * Todo script, migración y comando de prueba debe ejecutarse estrictamente dentro del entorno virtual local (`venv`) utilizando Python 3.12.10
  * Uso exclusivo de Django y Django REST Framework configurados según la arquitectura monolítica modular (`apps/accounts`, `apps/learning`, `apps/activities`, `apps/progress`).
  * Prohibido el uso de Docker durante la fase de desarrollo de la primera semana.
* **Entorno Frontend (Vue 3 / Vite):**
  * Uso de Vue 3 con Composition API (`<script setup>`).
  * Rutas declarativas en Vue Router y estado global gestionado mediante Pinia.
  * Estilos mediante CSS limpio y modular; animaciones controladas con Anime.js enfocadas únicamente en `transform` y `opacity` respetando la preferencia de movimiento reducido (`prefers-reduced-motion`).
* **Calidad y completitud del código:**
  * Cero tareas incompletas: no dejar bloques a medio hacer, funciones sin implementar ni pseudocódigo con comentarios `TODO` o `pass` sin autorización.
  * Todo código debe incluir manejo defensivo de errores, validación tipada o de serializadores y respuestas HTTP consistentes.

---

## 3. Integridad de Datos y Persistencia (MySQL)

* **Fuente única de verdad:** MySQL es la única base de datos del sistema para PARLIA. Queda prohibido mezclar o plantear motores NoSQL o estructuras paralelas.
* **Regla estricta de progreso de aprendizaje (`LearningProgress`):**
  * Debe existir una restricción única compuesta (`unique_together` o `UniqueConstraint`) entre `user` y `lesson`. Jamás se deben duplicar registros de avance para una misma lección.
  * La actualización del progreso se realiza mediante eventos explícitos del estudiante (por ejemplo: completar actividad o marcar lección terminada), nunca mediante peticiones continuas o sondeo masivo (*polling*) innecesario.
* **Almacenamiento multimedia:**
  * Prohibido almacenar binarios (imágenes pesadas, videos) directamente en la base de datos.
  * Durante el MVP, los recursos multimedia se gestionan exclusivamente como metadatos estructurados (título, tipo, URL externa confiable) en la tabla `MediaAsset`.

---

## 4. Seguridad Activa y Buenas Prácticas (No Negociable en el MVP)

La seguridad es parte integral del entregable inicial, no una tarea postergable:

1. **Aislamiento de credenciales:**
   * Secretos, claves de API, credenciales de MySQL y configuraciones sensibles residen estrictamente en variables de entorno (`.env`).
   * El archivo `.env` está expresamente excluido de Git vía `.gitignore`. Solo se versiona `.env.example` con nombres de variables y valores de plantilla no confidenciales.
2. **Control de acceso y permisos:**
   * Todo endpoint de la API bajo `/api/v1/` que involucre datos privados (progreso, actividades, perfil) debe exigir autenticación explícita y validar permisos en el backend.
   * La API debe impedir estrictamente ataques de referencia directa insegura a objetos (IDOR): ningún usuario podrá consultar ni alterar el progreso o respuestas de otro estudiante alterando parámetros en la URL.
3. **Autenticación protegida:**
   * Almacenamiento de contraseñas exclusivamente mediante el algoritmo seguro de hashing nativo de Django (PBKDF2 / Argon2). Prohibido el texto plano.
   * Si se implementa autenticación por sesiones/cookies, activar protección CSRF y flags `Secure`, `HttpOnly` y `SameSite`. Si se usan tokens, definir expiración y no almacenar tokens de larga duración en `localStorage` desprotegido.
4. **Configuración de producción:**
   * `DEBUG = False` en cualquier despliegue externo.
   * Definición explícita de dominios autorizados en `ALLOWED_HOSTS` y configuración estricta de encabezados CORS para aceptar únicamente el origen del frontend.
5. **Privacidad frente a Inteligencia Artificial:**
   * Cero envío de nombres, correos o datos identificables de estudiantes a proveedores externos de LLMs. Toda la experiencia de PARLIA en el MVP opera con contenido pedagógico estructurado y actividades locales.

---

## 5. Diseño y Ergonomía del Estudiante (Sin Punición)

* **Propósito formativo, no punitivo:** PARLIA es un entorno seguro de autoaprendizaje y alfabetización técnica para estudiantes de ingeniería. La interfaz y los mensajes del sistema deben incentivar el ensayo, la experimentación crítica y el aprendizaje sin generar ansiedad por notas o bloqueos restrictivos.
* **Contenido de los 6 módulos:** Toda estructura de lecciones debe respetar los 6 ejes pedagógicos definidos:
  1. Fundamentos de la Inteligencia Artificial Generativa
  2. Ingeniería de Prompts
  3. Verificaciones
  4. Ética, Privacidad e Integridad Académica
  5. Aplicacion en investigacion, redaccion
  6. Actividades finales 
* **Data-Ink Ratio y Usabilidad:**
  * Interfaz limpia, legible y completamente responsiva (móviles y escritorio).
  * Navegación clara con indicadores visibles de estado por lección (`pending`, `in_progress`, `completed`).
  * Las animaciones con Anime.js deben ser sutiles y no deben demorar ni entorpecer la interacción o lectura del contenido.

---

## 6. Bitácora de Proyecto y Trazabilidad

El agente mantendrá sincronizados los archivos de seguimiento del repositorio en cada iteración:

* **`docs/decisions.md` (ADRs):** Registrar inmediatamente cualquier decisión relevante acordada con el usuario, detallando contexto, alternativas descartadas, justificación técnica y consecuencias.
* **`docs/tasks.md`:** Actualizar de forma atómica el estado de cada tarea (`[ ] Pendiente`, `[/] En Progreso`, `[x] Completada`). No se inicia una tarea subsecuente sin cerrar y probar la tarea activa.
* **`docs/memory.md`:** Documentar en cada paso el estado vivo de la arquitectura, variables implementadas, endpoints disponibles y siguientes pasos inmediatos.

---

## 7. Ciclo de Ejecución del MVP (Plan de 7 Días)

El agente debe ceñirse rigurosamente al orden cronológico de trabajo:

```text
[  Repo + Base Local (Vue 3, Django, MySQL) ]
                    │
                    ▼
[  Modelos + Migraciones + Django Admin ]
                    │
                    ▼
[  API REST (Módulos, Lecciones, Auth, Progreso) ]
                    │
                    ▼
[  Frontend Base (Vistas, Rutas, Módulos y Lecciones) ]
                    │
                    ▼
[  Integración Auth + Pinia + Persistencia de Progreso ]
                    │
                    ▼
[  Actividades Simples + Estilos + Animaciones ]
                    │
                    ▼
[  Pruebas de Calidad + Seguridad + Configuración Piloto ]
```