# DESIGN: Guía de Estilo Visual, Arquitectura de Interfaz y Experiencia de Usuario (UI/UX)

**Proyecto:** PARLIA (Laboratorio Virtual de Aprendizaje en Inteligencia Artificial Generativa)  
**Institución:** Universidad de La Guajira - Facultad de Ingeniería  
**Línea Gráfica:** Identidad Institucional Uniguajira + Estética Futurista/Académica Limpia  
**Versión:** 1.0 (MVP 1 Semana)  
**Librería de Animación:** Anime.js 3.2+  

---

## 1. Identidad Cromática y Tokens de Diseño

La paleta cromática toma como base los colores emblemáticos e identitarios de la Universidad de La Guajira (Ocre Tierra, Aguamarina Caribe y Rosa Flamenco/Coral), combinados con fondos de alta luminosidad y tonos oscuros de alto contraste para maximizar la legibilidad en pantallas de computadores y dispositivos móviles.

### 1.1. Paleta Primaria (Colores Institucionales Uniguajira)

* **Ocre Tierra (Acento Primario y Logros):** `#C2822B` (Hover/Dark: `#9E671E`)  
  * *Semántica:* Identificador institucional de marca, hitos desbloqueados, botones de acción primaria y elementos activos.
* **Aguamarina Caribe (Secundario y Fluidez):** `#2A9D8F` (Hover/Dark: `#1F7369`)  
  * *Semántica:* Estados de lección "en progreso", enlaces secundarios, chips de carreras y trazado activo de la ruta.
* **Rosa Flamenco / Coral (Acento Dinámico y Banderas):** `#E76F51` (Hover/Dark: `#D45233`)  
  * *Semántica:* Banderas de check-point en el camino del progreso, etiquetas de advertencia técnica, tips y alertas no punitivas.

### 1.2. Superficies y Neutros (Modo Claro de Alto Data-Ink Ratio)

* **Fondo Principal de Aplicación:** `#F8F9FA` (Gris neutro de baja saturación, evita fatiga ocular).
* **Superficie de Tarjetas y Paneles (Cards):** `#FFFFFF` (Borde sutil `1px solid #E5E7EB` y sombra de elevación `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05)`).
* **Fondo de Sidebar Plegable y Topbar:** `#FFFFFF` (Integrado visualmente con una línea divisoria inferior y lateral `#E5E7EB`).
* **Texto Primario (High Contrast):** `#1F2937` (Gris carbón para títulos y textos de estudio).
* **Texto Secundario (Muted):** `#6B7280` (Metadatos, duraciones estimadas, subtítulos).
* **Éxito / Completado:** `#10B981` (Verde esmeralda para marcar check-points alcanzados).

---

## 2. Tipografía y Jerarquía Textual

Se prioriza el rendimiento y la legibilidad inmediata mediante fuentes de sistema modernas:

* **Familia Tipográfica:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`.
* **Encabezados Principales (H1):** `28px - 32px`, peso `700` (Bold), color `#1F2937`.
* **Títulos de Módulo y Vistas (H2):** `20px - 24px`, peso `600` (Semi-bold), color `#1F2937`.
* **Subtítulos y Nombres de Lección (H3):** `16px - 18px`, peso `600` (Semi-bold).
* **Texto de Contenido (Body):** `15px - 16px`, peso `400` (Regular), altura de línea `1.65` para facilitar lecturas extensas.
* **Micro-copias / Metadatos (Badges):** `12px - 13px`, peso `500` (Medium).

---

## 3. Arquitectura del Layout y Estructura Global

El lienzo se organiza en tres bloques principales: **Barra de Navegación Superior (Topbar)**, **Menú Lateral Desplegable (Collapsible Sidebar)** y **Área de Trabajo Central Dinámica**.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [≡] PARLIA  │  (Búsqueda rápida...)          [📺 Videos] [📰 Noticias] [🎯 Progreso] [👤 Perfil] │  <- TOPBAR (Fijo)
├───────────┬────────────────────────────────────────────────────────────────────────────┤
│ SIDEBAR   │                                                                            │
│ (Plegable)│                       ÁREA DE CONTENIDO DINÁMICA                           │
│           │                                                                            │
│ 🎓 Carrera│  [ Breadcrumb: Módulo 2 / Lección 1 ]                                      │
│  - Sistem.│                                                                            │
│  - Indust.│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  - Mecán. │  │                                                                      │  │
│  - Civil  │  │                     CONTENIDO DE LA VISTA                            │  │
│  - etc... │  │                                                                      │  │
│           │  │  (Ruta del Guerrero / Tarjetas de Módulos / Visor de Lección)        │  │
│ 🎨 Imagen │  │                                                                      │  │
│           │  │                                                                      │  │
│ ✍️ Redacc. │  │                                                                      │  │
│           │  │                                                                      │  │
│ 💡 Prompts│  └──────────────────────────────────────────────────────────────────────┘  │
│           │                                                                            │
└───────────┴────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Especificación Detallada de Componentes

### 4.1. Barra Superior (Topbar)

La barra superior permanece fija en la parte superior (`z-index: 50`) con una altura de `64px` y contiene los accesos rápidos universales:

1. **Botón Toggle de Menú:** Ícono tipo hamburguesa (`[≡]`) que contrae/expande el Sidebar con animación suave.
2. **Logotipo Institucional:** Logotipo de **PARLIA** junto al imagotipo de la Universidad de La Guajira.
3. **Las 4 Opciones de Navegación:**
   * **📺 Videos:** Catálogo curado de videos multimedia externos de alta calidad que profundizan en conceptos de IA generativa (sin abrumar con texto).
   * **📰 Noticias:** Feed dinámico y sintetizado con los últimos avances, papers y lanzamientos de IA en el mundo (tarjetas minimalistas con enlace a la fuente).
   * **🎯 Progreso:** Acceso directo a la **Ruta del Guerrero hacia la Montaña** (vista interactiva del viaje de aprendizaje).
   * **👤 Perfil:** Acceso a los datos del estudiante (nombre, correo `@uniguajira.edu.co`, programa académico e indicador de avance general).

### 4.2. Menú Lateral Plegable (Collapsible Sidebar)

El menú izquierdo tiene dos estados: **Expandido (`260px`)** y **Colapsado (`72px` o totalmente oculto en móviles)**. Permite acceder a áreas de contexto y cápsulas de apoyo rápido:

* **🎓 Carreras (Menú Desplegable / Acordeón):**
  * *Ingeniería de Sistemas* (Ejemplos de prompts y casos orientados a arquitectura de software, bases de datos y algoritmos).
  * *Ingeniería Industrial* (Casos de uso en optimización de operaciones, logística y análisis documental).
  * *Ingeniería Mecánica* (Soporte en documentación técnica, mantenimiento y modelado físico-matemático).
  * *Ingeniería Civil* (Especificaciones estructurales, normativas y redacción de memorias de cálculo).
* **🎨 Imágenes (Cápsula Informativa):**
  * Vista visual y concisa que explica cómo funcionan los modelos de difusión y generación de imágenes (Midjourney, DALL-E, Stable Diffusion), estructura de prompts visuales (estilo, iluminación, perspectiva) y consideraciones de propiedad intelectual.
  * **Regla estricta:** Esta vista es de consulta libre y **no computa dentro del porcentaje de progreso formal** del estudiante.
* **✍️ Redacción (Cápsula Informativa):**
  * Pautas de edición y sintetización de textos técnicos, técnicas de paráfrasis consciente y cómo utilizar la IA como asistente de redacción sin perder la voz analítica personal. Tampoco afecta el progreso formal.
* **💡 Prompts (Biblioteca de Patrones):**
  * Repositorio interactivo de plantillas de prompts probados y altamente eficientes para tareas generales de ingeniería (técnica del rol, pocos ejemplos / *few-shot*, desglose paso a paso / *chain-of-thought*). Cuenta con botón "Copiar al portapapeles" en un clic.

---

## 5. El Camino del Progreso: "La Expedición del Guerrero a la Montaña"

Inspirado en el concepto visual del camino serpenteante con conos y banderas, el progreso en PARLIA se transforma en una **metáfora visual e interactiva** donde el estudiante encarna a un **guerrero del conocimiento** que asciende por un sendero sinuoso hacia la **Cumbre de la Sabiduría (La Montaña)**.

### 5.1. Elementos Visuales del Mapa de Progreso

```text
                                         [ 🚩 META / LA CUMBRE ]
                                                ▲
                                               / \  (Nieve y Sol Dorado)
                                              /   \
                                             /     \
                                            /       \
                                    [Hito 6: Actividades finales ]
                                           \
                                            \  <- Tramo 5 (Curva Serpenteante)
                                             \
                                      [Hito 5: Aplicacion en investigacion, redaccion]
                                             /
                       Tramo 3 ->           /
                                  [Hito 4:Ética, Privacidad e Integridad Académica]
                                           \
                                            \
                                    [Hito 3: Verificaciones]
                                           /
                                          /  <- Tramo 2 (Sendero)
                                  [Hito 2: Prompt Engineering]
                                         \
                                          \
                                  [Hito 1: Fundamentos IA]
                                         ▲
                                         │  (Inicio / Campamento Base)
                                  [ 🏃 Avatar Guerrero ]
```

1. **El Sendero Serpenteante (Vector SVG Interactivo):**
   * Una línea continua SVG suavemente curvada que recorre el lienzo de abajo hacia arriba.
   * El tramo completado brilla en **Aguamarina Caribe (`#2A9D8F`)** o **Dorado Ocre (`#C2822B`)**.
   * El tramo por recorrer se muestra en gris punteado tenue (`#D1D5DB`).
2. **Los 6 Puntos de Control (Check-points / Hitos):**
   * Cada uno de los 6 módulos educativos es una estación o campamento en el sendero:
     1. *Campamento 1: Fundamentos de la IAG*
     2. *Campamento 2: Maestría en Prompts*
     3. *Campamento 3: Verificaciones*
     4. *Campamento 4: Ética, Privacidad e Integridad Académica*
     5. *Campamento 5: Aplicacion en investigacion, redaccion*
     6. *Campamento 6: Actividades finales *
   * **Banderas de Check-point:** Al completar un módulo, la bandera ondea en color Coral/Flamenco (`#E76F51`) con una pequeña insignia dorada.
3. **El Guerrero en Movimiento (Avatar SVG/Lottie):**
   * Un personaje estilizado minimalista que se sitúa dinámicamente en el hito correspondiente al progreso real del estudiante.
   * Al pasar de lección o completar una unidad, el guerrero camina por el sendero hasta la siguiente estación.
4. **La Cumbre (Meta Final):**
   * En la parte superior del mapa se erige la montaña iluminada con el sol dorado (`#FDDA24` / `#C2822B`), simbolizando el dominio ético y profesional de la IA para su carrera.

### 5.2. Orquestación de Animaciones con Anime.js

Anime.js se utiliza exclusivamente para dotar de vida este mapa interactivo sin ralentizar la interfaz:

* **Animación del Trazo del Sendero (`stroke-dashoffset`):**
  * El camino SVG se va dibujando progresivamente a medida que el estudiante ingresa a la vista:
  ```javascript
  anime({
    targets: '#path-progress',
    strokeDashoffset: [anime.setDashoffset, 0],
    easing: 'easeInOutSine',
    duration: 1500,
    delay: 200
  });
  ```
* **Desplazamiento del Guerrero:**
  * El avatar sigue las coordenadas paramétricas del trazado SVG usando `anime.path()`:
  ```javascript
  const path = anime.path('#path-progress');
  anime({
    targets: '#warrior-avatar',
    translateX: path('x'),
    translateY: path('y'),
    rotate: path('angle'),
    easing: 'easeOutElastic(1, .8)',
    duration: 2000
  });
  ```
* **Efecto de Hito Desbloqueado:**
  * Al marcar una lección o módulo como completado, el ícono del campamento realiza un sutil rebote con partículas doradas (`scale: [0.8, 1.2, 1]`).
* **Micro-interacción Hover:**
  * Al posar el cursor sobre cualquier campamento en el mapa, se despliega una tarjeta flotante minimalista con el título, cantidad de lecciones completadas y un botón rápido: *"Continuar ascenso"*.

---

## 6. Principios Antirruido y Criterios de Dinamismo

Para garantizar que el sitio se sienta dinámico sin sobrecargarse de información:

1. **Cero Muros de Texto:** El contenido educativo se fracciona en bloques de lectura de máximo 3 a 5 párrafos, intercalados con recuadros de código interactivo, llamadas de atención (*callouts*) y analogías gráficas.
2. **Espaciado Generoso (Whitespace):** Uso consistente de un sistema de espaciado modular (`p-4`, `p-6`, `p-8` o múltiplos de `8px`), dejando respirar los componentes.
3. **Divulgación Progresiva:** En la biblioteca de prompts y vistas de carreras, los ejemplos complejos se encuentran ocultos bajo pestañas o tarjetas plegables para que el estudiante explore únicamente lo que necesita sin saturar su campo visual.
4. **Respeto a Preferencias del Usuario:** Toda animación de Anime.js está condicionada a `@media (prefers-reduced-motion: reduce)`. Si el estudiante tiene desactivadas las animaciones en su sistema operativo, el mapa se presenta de forma estática instantánea con los estados finales correspondientes.
5. **Transiciones Rápidas:** Las transiciones de ruta y aperturas de modales tienen una duración máxima de `250ms - 300ms` usando curvas tipo `ease-out`.

---

## 7. Responsive Design y Breakpoints

* **Desktop Grande (`≥ 1280px`):** Sidebar expandido por defecto (`260px`), mapa del sendero en orientación vertical-diagonal con detalles completos.
* **Laptop / Tablet (`768px - 1279px`):** Sidebar colapsado en modo íconos (`72px`), el mapa de la montaña se adapta en escala fluida.
* **Móvil (`< 768px`):** 
  * Sidebar completamente oculto tipo cajón (*Drawer* deslizante con fondo oscuro translúcido al presionar el botón `[≡]`).
  * Los 4 botones de la Topbar se transforman en íconos limpios con tooltip.
  * El sendero de la montaña adopta una vista vertical optimizada para scroll táctil.