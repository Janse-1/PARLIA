<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import anime from 'animejs/lib/anime.es.js'
import { useAuthStore } from '../stores/auth'

import localHeroVideo from '../assets/gemini_generated_video_0609d70b.mp4'
import paraAnimarImg from '../assets/para_animar.jpeg'

const router = useRouter()
const authStore = useAuthStore()

const currentLang = ref(localStorage.getItem('parlia_lang') || 'ES')
const mobileMenuOpen = ref(false)
const scrollTrackRef = ref(null)
const synapseStageRef = ref(null)

// Progreso del scroll con interpolación suave (60fps)
const rawScrollProgress = ref(0)
const smoothScrollProgress = ref(0)
let scrollTimeline = null
let rafId = null

const i18n = {
  ES: {
    nav: {
      synapse: 'Sinapsis Cognitiva',
      pillars: 'Pilares Formativos',
      methodology: 'Metodología Crítica',
      audit: 'Auditoría Viva',
      identity: 'Identidad Uniguajira',
    },
    exploreBtn: 'Ingresar al Laboratorio',
    heroBadge: 'FACULTAD DE INGENIERÍA · UNIVERSIDAD DE LA GUAJIRA',
    heroTitleLine1: 'Criterio Humano.',
    heroTitleLine2: 'Potencia Algorítmica.',
    heroTitleLine3: 'Ingeniería Sin Atajos.',
    heroDesc:
      'ParLIA es el laboratorio cognitivo de Inteligencia Artificial Generativa diseñado para que el estudiante de ingeniería domine el razonamiento analítico, audite alucinaciones técnicas y utilice modelos de lenguaje con ética transparente y cero temor punitivo.',
    primaryCtaGuest: 'Iniciar Sesión',
    secondaryCtaGuest: 'Crear Cuenta Estudiantil',
    primaryCtaAuth: 'Continuar en el Laboratorio',
    secondaryCtaAuth: 'Explorar Sinapsis',
    heroStats: [
      { value: 'No Punitivo', label: 'Aprendizaje basado en reflexión y error seguro' },
      { value: 'Verificable', label: 'Contrastación rigurosa de código, teoremas y normas' },
      { value: 'Sello Wayuu', label: 'Tejido entre saber ancestral y frontera digital' },
    ],
    synapseSection: {
      badge: 'TRANSFERENCIA COGNITIVA EN TIEMPO REAL',
      title: 'Del Fundamento Teórico a la Red Neuronal Crítica',
      subtitle:
        'Desplázate para observar cómo ParLIA articula el conocimiento analógico de la ingeniería con la mediación humana y la inferencia generativa.',
      phases: [
        {
          code: 'NODO 01 // FUNDAMENTACIÓN',
          title: 'Dominio del Fenómeno Físico y Matemático',
          desc: 'Antes de escribir un prompt, el estudiante comprende las leyes, restricciones de diseño y variables reales del problema desde la literatura científica.',
        },
        {
          code: 'NODO 02 // MEDIACIÓN Y ARQUITECTURA',
          title: 'Formulación Técnica Estructurada',
          desc: 'El ingeniero traduce su modelo mental en instrucciones de alta precisión: define contexto operativo, rol técnico, formato y límites de seguridad.',
        },
        {
          code: 'NODO 03 // AUDITORÍA ALGORÍTMICA',
          title: 'Verificación Contra Alucinaciones y Sesgos',
          desc: 'La respuesta del modelo nunca es el punto final: se somete a pruebas unitarias, validación dimensional y contrastación bibliográfica.',
        },
      ],
      hudTags: [
        '01 · LITERATURA Y TEOREMAS',
        '02 · MEDIACIÓN Y PROMPTING',
        '03 · CÓRTEX Y VERIFICACIÓN',
      ],
    },
    pillarsSection: {
      badge: 'ECOSISTEMA PEDAGÓGICO PARLIA',
      title: 'Cuatro Dimensiones para una Alfabetización Real en IA',
      desc: 'A diferencia de un curso convencional, ParLIA entrena el juicio profesional frente a sistemas probabilísticos.',
      cards: [
        {
          num: '01',
          tag: 'Razonamiento Primero',
          title: 'Desacople de la Dependencia Cognitiva',
          desc: 'Evitamos el hábito de copiar y pegar sin comprender. Cada actividad exige formular hipótesis propias antes de consultar al modelo.',
        },
        {
          num: '02',
          tag: 'Ingeniería de Contexto',
          title: 'Diseño de Prompts de Grado Industrial',
          desc: 'Estructuración modular con restricciones de complejidad temporal, normativas técnicas (NSR, IEEE, ISO) y validación paso a paso.',
        },
        {
          num: '03',
          tag: 'Escepticismo Científico',
          title: 'Detección de Alucinaciones y Código Frágil',
          desc: 'Entrenamiento práctico para identificar librerías inexistentes, vulnerabilidades ocultas, citas apócrifas y errores sutiles de lógica.',
        },
        {
          num: '04',
          tag: 'Integridad Académica',
          title: 'Trazabilidad y Declaración Transparente',
          desc: 'Aprende cuándo, cómo y por qué declarar el uso de IA generativa en proyectos de investigación, informes técnicos y desarrollo de software.',
        },
      ],
    },
    methodologySection: {
      badge: 'CICLO DE TRABAJO EN PARLIA',
      title: 'El Protocolo de Verificación en 4 Etapas',
      desc: 'Un flujo sistemático y centrado en el estudiante para convertir cada consulta en aprendizaje de ingeniería verificable.',
      steps: [
        {
          step: 'ETAPA 01',
          name: 'Comprensión Autónoma',
          detail: 'Delimitación matemática y conceptual del reto sin asistencia automatizada.',
        },
        {
          step: 'ETAPA 02',
          name: 'Instrucción con Restricciones',
          detail: 'Construcción del prompt especificando supuestos, bordes y criterios de éxito.',
        },
        {
          step: 'ETAPA 03',
          name: 'Inspección y Pruebas',
          detail: 'Ejecución de casos límite, revisión de referencias y detección de fallos lógicos.',
        },
        {
          step: 'ETAPA 04',
          name: 'Síntesis y Autoría Propia',
          detail: 'Documentación reflexiva del aprendizaje adquirido y declaración ética de uso.',
        },
      ],
    },
    auditSection: {
      badge: 'ANATOMÍA DE UNA INTERACCIÓN CRÍTICA',
      title: 'No Aceptes Respuestas A Ciegas: Audítalas',
      desc: 'Observa la diferencia entre el uso pasivo de un chatbot y el enfoque de ingeniería asistida que practicamos dentro de ParLIA.',
      naiveLabel: 'CONSULTA EMPÍRICA (RIESGO DE ALUCINACIÓN)',
      naivePrompt:
        '"Hazme el código en Python para calcular la pérdida de carga en una tubería y dame 3 referencias IEEE."',
      naiveIssue:
        'Resultado: Ecuación de factor de fricción mal aplicada en régimen turbulento y 2 DOI inventados por el modelo.',
      parliaLabel: 'PROTOCOLO PARLIA (INGENIERÍA VERIFICADA)',
      parliaPrompt:
        '"Actúa como revisor hidráulico. Dado Re = 1.4e5 y rugosidad ε/D = 0.0002, compara la aproximación explícita de Swamee-Jain frente a Colebrook-White y genera un test unitario que verifique el error relativo < 1%."',
      parliaResult:
        'Resultado: Parámetros acotados, convergencia numérica comprobable y criterio de aceptación auditable por el estudiante.',
    },
    identitySection: {
      badge: 'IDENTIDAD CULTURAL Y TECNOLOGICA',
      title: 'Kanas Wayuu y Redes Neuronales: El Tejido del Pensamiento',
      p1: 'En la cosmovisión Wayuu, el Kanas es el arte de tejer figuras geométricas complejas donde cada hilo cumple una función estructural y simbólica. En ParLIA honramos esa herencia desde La Guajira: programar y dialogar con la inteligencia artificial también es tejer estructuras lógicas con propósito.',
      p2: 'Nuestra plataforma nace en la Facultad de Ingeniería de la Universidad de La Guajira para demostrar que desde nuestra región construimos soberanía tecnológica, pensamiento crítico y rigor científico de primer nivel.',
    },
    ctaBox: {
      badge: 'LABORATORIO VIRTUAL PARLIA',
      title: 'Comienza tu Recorrido Formativo en ParLIA',
      desc: 'Accede con tu cuenta estudiantil o regístrate en segundos para desbloquear el laboratorio completo.',
    },
    footerCredits:
      'Laboratorio Virtual de Aprendizaje en IA Generativa · Facultad de Ingeniería · Universidad de La Guajira',
  },
  EN: {
    nav: {
      synapse: 'Cognitive Synapse',
      pillars: 'Formative Pillars',
      methodology: 'Critical Methodology',
      audit: 'Live Audit',
      identity: 'Uniguajira Identity',
    },
    exploreBtn: 'Enter Laboratory',
    heroBadge: 'FACULTY OF ENGINEERING · UNIVERSIDAD DE LA GUAJIRA',
    heroTitleLine1: 'Human Judgment.',
    heroTitleLine2: 'Algorithmic Power.',
    heroTitleLine3: 'Engineering Without Shortcuts.',
    heroDesc:
      'ParLIA is the Generative AI cognitive laboratory designed for engineering students to master analytical reasoning, audit technical hallucinations, and use language models with transparent ethics and zero punitive fear.',
    primaryCtaGuest: 'Sign In',
    secondaryCtaGuest: 'Create Student Account',
    primaryCtaAuth: 'Continue in Laboratory',
    secondaryCtaAuth: 'Explore Synapse',
    heroStats: [
      { value: 'Non-Punitive', label: 'Learning built on reflection and safe experimentation' },
      { value: 'Verifiable', label: 'Rigorous verification of code, theorems, and standards' },
      { value: 'Wayuu Heritage', label: 'Weaving ancestral geometry with digital frontiers' },
    ],
    synapseSection: {
      badge: 'REAL-TIME COGNITIVE TRANSFER',
      title: 'From Theoretical Foundations to Critical Neural Networks',
      subtitle:
        'Scroll down to experience how ParLIA bridges analog engineering knowledge with human mediation and generative inference.',
      phases: [
        {
          code: 'NODE 01 // FOUNDATIONS',
          title: 'Mastery of Physical & Mathematical Phenomena',
          desc: 'Before writing a prompt, the student understands the governing laws, design constraints, and real variables from primary scientific literature.',
        },
        {
          code: 'NODE 02 // MEDIATION & ARCHITECTURE',
          title: 'Structured Technical Formulation',
          desc: 'The engineer translates mental models into high-precision instructions: defining operational context, technical role, output schema, and safety bounds.',
        },
        {
          code: 'NODE 03 // ALGORITHMIC AUDIT',
          title: 'Verification Against Hallucinations & Bias',
          desc: 'Model output is never the final step: it undergoes unit testing, dimensional analysis, and bibliographic cross-checking.',
        },
      ],
      hudTags: [
        '01 · LITERATURE & THEOREMS',
        '02 · MEDIATION & PROMPTING',
        '03 · CORTEX & VERIFICACIÓN',
      ],
    },
    pillarsSection: {
      badge: 'PARLIA PEDAGOGICAL ECOSYSTEM',
      title: 'Four Dimensions for True AI Literacy',
      desc: 'Unlike conventional courses, ParLIA trains professional engineering judgment when interacting with probabilistic systems.',
      cards: [
        {
          num: '01',
          tag: 'Reasoning First',
          title: 'Decoupling Cognitive Dependency',
          desc: 'We eliminate blind copy-pasting. Every activity requires formulating your own hypothesis before querying the model.',
        },
        {
          num: '02',
          tag: 'Context Engineering',
          title: 'Industrial-Grade Prompt Design',
          desc: 'Modular structuring with time-complexity constraints, engineering standards (NSR, IEEE, ISO), and step-by-step verification.',
        },
        {
          num: '03',
          tag: 'Scientific Skepticism',
          title: 'Detecting Hallucinations & Fragile Code',
          desc: 'Hands-on training to spot non-existent libraries, hidden vulnerabilities, apocryphal citations, and subtle logic flaws.',
        },
        {
          num: '04',
          tag: 'Academic Integrity',
          title: 'Traceability & Transparent Disclosure',
          desc: 'Learn when, how, and why to disclose generative AI usage in research papers, technical reports, and software engineering.',
        },
      ],
    },
    methodologySection: {
      badge: 'PARLIA WORKFLOW CYCLE',
      title: 'The 4-Stage Verification Protocol',
      desc: 'A systematic, student-centered workflow turning every query into verifiable engineering learning.',
      steps: [
        {
          step: 'STAGE 01',
          name: 'Autonomous Comprehension',
          detail: 'Mathematical and conceptual framing of the challenge without automated assistance.',
        },
        {
          step: 'STAGE 02',
          name: 'Constrained Instruction',
          detail: 'Building the prompt by specifying assumptions, edge cases, and acceptance criteria.',
        },
        {
          step: 'STAGE 03',
          name: 'Inspection & Testing',
          detail: 'Running boundary tests, checking citations, and catching logical flaws.',
        },
        {
          step: 'STAGE 04',
          name: 'Synthesis & Authorship',
          detail: 'Reflective documentation of acquired learning and ethical disclosure.',
        },
      ],
    },
    auditSection: {
      badge: 'ANATOMY OF A CRITICAL INTERACTION',
      title: 'Never Accept Outputs Blindly: Audit Them',
      desc: 'Compare passive chatbot usage with the verified engineering workflow practiced inside ParLIA.',
      naiveLabel: 'EMPIRICAL QUERY (HALLUCINATION RISK)',
      naivePrompt:
        '"Write Python code to calculate pipe head loss and give me 3 IEEE references."',
      naiveIssue:
        'Outcome: Friction factor equation misapplied in turbulent regime and 2 fabricated DOIs.',
      parliaLabel: 'PARLIA PROTOCOL (VERIFIED ENGINEERING)',
      parliaPrompt:
        '"Act as a hydraulic reviewer. Given Re = 1.4e5 and roughness ε/D = 0.0002, compare the explicit Swamee-Jain approximation against Colebrook-White and generate a unit test verifying relative error < 1%."',
      parliaResult:
        'Outcome: Bounded parameters, verifiable numerical convergence, and student-auditable acceptance criteria.',
    },
    identitySection: {
      badge: 'CULTURAL & TECHNOLOGICAL IDENTITY',
      title: 'Wayuu Kanas & Neural Networks: Weaving Thought',
      p1: 'In the Wayuu worldview, Kanas is the art of weaving intricate geometric patterns where every thread serves a structural and symbolic purpose. At ParLIA, we honor this heritage from La Guajira: programming and dialoguing with artificial intelligence is also weaving logical structures with purpose.',
      p2: 'Born at the Faculty of Engineering of Universidad de La Guajira, our platform demonstrates that from our region we build technological sovereignty, critical thinking, and world-class scientific rigor.',
    },
    ctaBox: {
      badge: 'PARLIA VIRTUAL LABORATORY',
      title: 'Begin Your Formative Journey in ParLIA',
      desc: 'Sign in with your student account or register in seconds to unlock the full laboratory.',
    },
    footerCredits:
      'Generative AI Virtual Learning Lab · Faculty of Engineering · Universidad de La Guajira',
  },
}

const t = computed(() => i18n[currentLang.value] || i18n.ES)

const activeScrollPhase = computed(() => {
  if (smoothScrollProgress.value < 0.34) return 0
  if (smoothScrollProgress.value < 0.68) return 1
  return 2
})

function setLanguage(lang) {
  currentLang.value = lang
  localStorage.setItem('parlia_lang', lang)
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

function handleExplorePlatform() {
  closeMobileMenu()
  if (authStore.isAuthenticated) {
    router.push('/modules')
  } else {
    router.push('/login')
  }
}

function initScrollTimeline() {
  if (!synapseStageRef.value) return

  const beamPaths = synapseStageRef.value.querySelectorAll('.synapse-beam')
  beamPaths.forEach((p) => {
    const len = p.getTotalLength ? p.getTotalLength() : 600
    p.style.strokeDasharray = `${len}`
    p.style.strokeDashoffset = `${len}`
  })

  scrollTimeline = anime.timeline({
    autoplay: false,
    duration: 1000,
    easing: 'linear',
  })

  // 1. Escala y perspectiva progresiva de toda la obra `para_animar.jpeg` centrada y grande
  scrollTimeline.add(
    {
      targets: '.synapse-art-wrapper',
      scale: [0.94, 1.02],
      rotateX: [5, 0],
      translateY: [12, -4],
      duration: 1000,
      easing: 'easeInOutSine',
    },
    0
  )

  // 2. Desplazamiento de la máscara de iluminación (Spotlight) desde Libros (Izquierda) -> Estudiante (Centro) -> Cerebro IA (Derecha)
  scrollTimeline.add(
    {
      targets: '.synapse-spotlight-layer',
      opacity: [0.3, 1],
      duration: 280,
      easing: 'easeOutQuad',
    },
    0
  )

  // 3. Etapa 1 (0 -> 350): Encendido de la Zona de Libros + Haz de transferencia hacia la estudiante
  scrollTimeline.add(
    {
      targets: '.beam-books-to-student',
      strokeDashoffset: [anime.setDashoffset, 0],
      opacity: [0.2, 1],
      duration: 360,
      easing: 'easeInOutCubic',
    },
    20
  )

  scrollTimeline.add(
    {
      targets: '.ring-books',
      scale: [0.4, 1],
      opacity: [0, 1],
      rotate: ['-45deg', '0deg'],
      duration: 320,
      easing: 'easeOutBack',
    },
    0
  )

  // 4. Etapa 2 (330 -> 680): Encendido del Nodo de Mediación Humana (Estudiante + Portátil) + Haz hacia el Córtex
  scrollTimeline.add(
    {
      targets: '.beam-student-to-brain',
      strokeDashoffset: [anime.setDashoffset, 0],
      opacity: [0.2, 1],
      duration: 360,
      easing: 'easeInOutCubic',
    },
    330
  )

  scrollTimeline.add(
    {
      targets: '.ring-student',
      scale: [0.4, 1],
      opacity: [0, 1],
      rotate: ['45deg', '0deg'],
      duration: 320,
      easing: 'easeOutBack',
    },
    320
  )

  // 5. Etapa 3 (650 -> 1000): Explosión sináptica en el Cerebro IA (Derecha) y anillos de telemetría
  scrollTimeline.add(
    {
      targets: '.beam-brain-cortex',
      strokeDashoffset: [anime.setDashoffset, 0],
      opacity: [0.2, 1],
      duration: 350,
      delay: anime.stagger(40),
      easing: 'easeInOutCubic',
    },
    640
  )

  scrollTimeline.add(
    {
      targets: '.ring-brain',
      scale: [0.4, 1.06, 1],
      opacity: [0, 1],
      rotate: ['-90deg', '0deg'],
      duration: 340,
      easing: 'easeOutBack',
    },
    650
  )

  scrollTimeline.add(
    {
      targets: '.cortex-spark',
      scale: [0, 1.35, 1],
      opacity: [0, 1],
      duration: 260,
      delay: anime.stagger(35),
      easing: 'easeOutBack',
    },
    690
  )
}

function handleWindowScroll() {
  if (!scrollTrackRef.value) return
  const rect = scrollTrackRef.value.getBoundingClientRect()
  const windowH = window.innerHeight
  const scrollableDistance = rect.height - windowH
  if (scrollableDistance <= 0) return

  const currentScrolled = -rect.top
  rawScrollProgress.value = Math.max(0, Math.min(1, currentScrolled / scrollableDistance))
}

function updateAnimationLoop() {
  const diff = rawScrollProgress.value - smoothScrollProgress.value
  if (Math.abs(diff) > 0.0003) {
    smoothScrollProgress.value += diff * 0.12
    if (scrollTimeline) {
      scrollTimeline.seek(smoothScrollProgress.value * scrollTimeline.duration)
    }
  }
  rafId = window.requestAnimationFrame(updateAnimationLoop)
}

// Coordenada dinámica del foco de luz (de 16% izquierda a 80% derecha según el scroll)
const spotlightX = computed(() => {
  return Math.round(16 + smoothScrollProgress.value * 64)
})

onMounted(async () => {
  await nextTick()
  initScrollTimeline()
  handleWindowScroll()
  smoothScrollProgress.value = rawScrollProgress.value
  if (scrollTimeline) {
    scrollTimeline.seek(smoothScrollProgress.value * scrollTimeline.duration)
  }
  window.addEventListener('scroll', handleWindowScroll, { passive: true })
  window.addEventListener('resize', handleWindowScroll, { passive: true })
  rafId = window.requestAnimationFrame(updateAnimationLoop)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleWindowScroll)
  window.removeEventListener('resize', handleWindowScroll)
  if (rafId) {
    window.cancelAnimationFrame(rafId)
  }
})
</script>

<template>
  <div class="parlia-landing">
    <!-- CAPA DE VIDEO LOCAL Y GRILLA ESPACIAL FIJA DE FONDO -->
    <div class="background-stage" aria-hidden="true">
      <video
        class="background-video"
        :src="localHeroVideo"
        autoplay
        muted
        loop
        playsinline
      />
      <div class="background-video-scrim" />
      <div class="background-grid" />
      <div class="background-glow glow-cyan" />
      <div class="background-glow glow-coral" />
    </div>

    <!-- BARRA DE NAVEGACIÓN FLOTANTE GLASSMORPHISM (RESPONSIVA) -->
    <header class="landing-navbar">
      <router-link to="/" class="brand-logo" @click="closeMobileMenu">
        <img src="/logo_parlia.png" alt="ParLIA Logo" class="brand-logo-img" />
        <span class="brand-logo-text">Par<span class="brand-highlight">LIA</span></span>
      </router-link>

      <nav class="landing-nav-links" aria-label="Navegación principal">
        <a href="#synapse">{{ t.nav.synapse }}</a>
        <a href="#pillars">{{ t.nav.pillars }}</a>
        <a href="#methodology">{{ t.nav.methodology }}</a>
        <a href="#audit">{{ t.nav.audit }}</a>
        <a href="#identity">{{ t.nav.identity }}</a>
      </nav>

      <div class="navbar-actions">
        <div class="lang-selector" role="group" aria-label="Idioma">
          <button
            type="button"
            class="lang-btn"
            :class="{ active: currentLang === 'EN' }"
            @click="setLanguage('EN')"
          >
            EN
          </button>
          <button
            type="button"
            class="lang-btn"
            :class="{ active: currentLang === 'ES' }"
            @click="setLanguage('ES')"
          >
            ES
          </button>
        </div>

        <button type="button" class="nav-cta-button desktop-only-btn" @click="handleExplorePlatform">
          {{ t.exploreBtn }}
        </button>

        <!-- Botón de menú móvil -->
        <button
          type="button"
          class="mobile-menu-toggle"
          :aria-expanded="mobileMenuOpen"
          aria-label="Abrir menú de navegación"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <svg v-if="!mobileMenuOpen" width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M4 7H20M4 12H20M4 17H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
          <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M6 6L18 18M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </button>
      </div>

      <!-- Drawer desplegable para móviles -->
      <div v-if="mobileMenuOpen" class="mobile-nav-drawer">
        <a href="#synapse" @click="closeMobileMenu">{{ t.nav.synapse }}</a>
        <a href="#pillars" @click="closeMobileMenu">{{ t.nav.pillars }}</a>
        <a href="#methodology" @click="closeMobileMenu">{{ t.nav.methodology }}</a>
        <a href="#audit" @click="closeMobileMenu">{{ t.nav.audit }}</a>
        <a href="#identity" @click="closeMobileMenu">{{ t.nav.identity }}</a>
        <div class="mobile-drawer-ctas">
          <button type="button" class="primary-button full-width" @click="handleExplorePlatform">
            {{ t.exploreBtn }}
          </button>
        </div>
      </div>
    </header>

    <main class="landing-main">
      <!-- 1. SECCIÓN HERO (CON EL CONTENIDO DE PARLIA + TIPOGRAFÍA MONUMENTAL) -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="pill-tag">{{ t.heroBadge }}</div>

          <h1 class="hero-display-title">
            <span>{{ t.heroTitleLine1 }}</span>
            <span class="title-accent-gradient">{{ t.heroTitleLine2 }}</span>
            <span>{{ t.heroTitleLine3 }}</span>
          </h1>

          <p class="hero-description">{{ t.heroDesc }}</p>

          <div class="hero-buttons">
            <template v-if="!authStore.isAuthenticated">
              <router-link to="/login" class="primary-button">
                {{ t.primaryCtaGuest }}
              </router-link>
              <router-link to="/register" class="secondary-button">
                {{ t.secondaryCtaGuest }}
              </router-link>
            </template>

            <template v-else>
              <router-link to="/modules" class="primary-button">
                {{ t.primaryCtaAuth }}
              </router-link>
              <a href="#synapse" class="secondary-button">
                {{ t.secondaryCtaAuth }}
              </a>
            </template>
          </div>

          <div class="hero-stats">
            <div v-for="(st, idx) in t.heroStats" :key="idx" class="stat-card">
              <h3>{{ st.value }}</h3>
              <span>{{ st.label }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. ANIMACIÓN INTERACTIVA DE SCROLL CENTRAL Y GRANDE CON `para_animar.jpeg` -->
      <section id="synapse" ref="scrollTrackRef" class="anime-scroll-track">
        <div class="anime-scroll-sticky">
          <div class="scroll-header-centered">
            <span class="pill-tag">{{ t.synapseSection.badge }}</span>
            <h2 class="scroll-section-title">{{ t.synapseSection.title }}</h2>
            <p class="scroll-section-sub">{{ t.synapseSection.subtitle }}</p>
          </div>

          <div class="scroll-stage-centered">
            <!-- Lienzo Central de Gran Formato con `para_animar.jpeg` -->
            <div ref="synapseStageRef" class="synapse-art-wrapper">
              <!-- Capa base tenue para dar contraste profundo -->
              <img
                :src="paraAnimarImg"
                alt="Base cognitiva ParLIA"
                class="para-animar-dimmed"
                aria-hidden="true"
              />

              <!-- Capa vibrante que se ilumina de izquierda a derecha con el scroll -->
              <div
                class="synapse-spotlight-layer"
                :style="{
                  '--spot-x': `${spotlightX}%`,
                }"
              >
                <img
                  :src="paraAnimarImg"
                  alt="Conexión entre libros de ingeniería, estudiante e Inteligencia Artificial"
                  class="para-animar-lit"
                />
              </div>

              <!-- Etiquetas HUD flotantes sobre las 3 zonas de la ilustración -->
              <div class="floating-hud hud-left" :class="{ active: activeScrollPhase >= 0 }">
                <span class="hud-dot dot-ochre" />
                <span>{{ t.synapseSection.hudTags[0] }}</span>
              </div>

              <div class="floating-hud hud-center" :class="{ active: activeScrollPhase >= 1 }">
                <span class="hud-dot dot-coral" />
                <span>{{ t.synapseSection.hudTags[1] }}</span>
              </div>

              <div class="floating-hud hud-right" :class="{ active: activeScrollPhase >= 2 }">
                <span class="hud-dot dot-cyan" />
                <span>{{ t.synapseSection.hudTags[2] }}</span>
              </div>

              <!-- Vectores de Telemetría y Haces de Energía Alineados con la Ilustración -->
              <svg
                viewBox="0 0 1000 720"
                class="synapse-svg-overlay"
                aria-hidden="true"
              >
                <defs>
                  <linearGradient id="beamGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#F99D1C" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="#FF5B26" stop-opacity="0.95" />
                  </linearGradient>
                  <linearGradient id="beamGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#FF5B26" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="#20A4B8" stop-opacity="0.95" />
                  </linearGradient>
                  <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="5" result="blur" />
                    <feMerge>
                      <feMergeNode in="blur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                </defs>

                <!-- Anillo de Telemetría 1: Libros y Fundamentos (Izquierda) -->
                <g class="ring-books" style="transform-origin: 210px 410px">
                  <circle
                    cx="210"
                    cy="410"
                    r="56"
                    fill="none"
                    stroke="#F99D1C"
                    stroke-width="1.8"
                    stroke-dasharray="8 6"
                    opacity="0.75"
                  />
                  <circle cx="210" cy="410" r="6" fill="#F99D1C" filter="url(#neonGlow)" />
                </g>

                <!-- Haz 1: Transferencia desde los Libros hacia la Estudiante -->
                <path
                  class="synapse-beam beam-books-to-student"
                  d="M 265 405 C 315 395, 345 365, 385 350"
                  fill="none"
                  stroke="url(#beamGrad1)"
                  stroke-width="3.5"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                />
                <path
                  class="synapse-beam beam-books-to-student"
                  d="M 295 250 C 340 250, 370 285, 395 320"
                  fill="none"
                  stroke="#F99D1C"
                  stroke-width="2.5"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                />

                <!-- Anillo de Telemetría 2: Mediación Humana y Portátil (Centro) -->
                <g class="ring-student" style="transform-origin: 415px 350px">
                  <circle
                    cx="415"
                    cy="350"
                    r="62"
                    fill="none"
                    stroke="#FF5B26"
                    stroke-width="1.8"
                    stroke-dasharray="10 6"
                    opacity="0.8"
                  />
                  <circle cx="485" cy="410" r="7" fill="#20A4B8" filter="url(#neonGlow)" />
                </g>

                <!-- Haz 2: De la Estudiante/Portátil hacia el Córtex del Cerebro IA -->
                <path
                  class="synapse-beam beam-student-to-brain"
                  d="M 485 410 C 535 405, 575 370, 625 325"
                  fill="none"
                  stroke="url(#beamGrad2)"
                  stroke-width="4"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                />
                <path
                  class="synapse-beam beam-student-to-brain"
                  d="M 470 305 C 525 275, 575 265, 635 260"
                  fill="none"
                  stroke="#20A4B8"
                  stroke-width="3"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                />

                <!-- Anillo de Telemetría 3 y Pulsos del Córtex IA (Derecha) -->
                <g class="ring-brain" style="transform-origin: 715px 315px">
                  <circle
                    cx="715"
                    cy="315"
                    r="118"
                    fill="none"
                    stroke="#20A4B8"
                    stroke-width="1.8"
                    stroke-dasharray="14 8"
                    opacity="0.7"
                  />
                  <circle
                    cx="715"
                    cy="315"
                    r="74"
                    fill="none"
                    stroke="#F99D1C"
                    stroke-width="1.4"
                    stroke-dasharray="6 8"
                    opacity="0.65"
                  />
                </g>

                <path
                  class="synapse-beam beam-brain-cortex"
                  d="M 625 325 C 665 270, 725 255, 785 285 C 830 310, 825 375, 765 405 C 710 430, 655 395, 625 325"
                  fill="none"
                  stroke="#20A4B8"
                  stroke-width="3"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                />

                <!-- Destellos puntuales sobre los nodos reales del cerebro de la ilustración -->
                <circle class="cortex-spark" cx="635" cy="260" r="7" fill="#FF5B26" filter="url(#neonGlow)" />
                <circle class="cortex-spark" cx="710" cy="235" r="8" fill="#20A4B8" filter="url(#neonGlow)" />
                <circle class="cortex-spark" cx="785" cy="285" r="8" fill="#F99D1C" filter="url(#neonGlow)" />
                <circle class="cortex-spark" cx="765" cy="405" r="7" fill="#20A4B8" filter="url(#neonGlow)" />
                <circle class="cortex-spark" cx="695" cy="340" r="9" fill="#FF5B26" filter="url(#neonGlow)" />
              </svg>
            </div>

            <!-- 3 Tarjetas de Nodos Cognitivos Alineadas Debajo de la Ilustración Central -->
            <div class="scroll-phases-row">
              <article
                v-for="(phase, idx) in t.synapseSection.phases"
                :key="phase.code"
                class="scroll-phase-card"
                :class="{ active: activeScrollPhase === idx }"
              >
                <span class="phase-step-code">{{ phase.code }}</span>
                <h3>{{ phase.title }}</h3>
                <p>{{ phase.desc }}</p>
              </article>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. PILARES FORMATIVOS DE PARLIA (LAS 4 DIMENSIONES REALES) -->
      <section id="pillars" class="section-spacing">
        <div class="section-header">
          <span class="pill-tag">{{ t.pillarsSection.badge }}</span>
          <h2>{{ t.pillarsSection.title }}</h2>
          <p>{{ t.pillarsSection.desc }}</p>
        </div>

        <div class="pillars-grid">
          <article v-for="card in t.pillarsSection.cards" :key="card.num" class="tech-card">
            <div class="card-top-row">
              <span class="card-number">{{ card.num }}</span>
              <span class="card-badge-tag">{{ card.tag }}</span>
            </div>
            <h3>{{ card.title }}</h3>
            <p>{{ card.desc }}</p>
          </article>
        </div>
      </section>

      <!-- 4. METODOLOGÍA CRÍTICA (4 ETAPAS CENTRADAS Y ORGANIZADAS EN DESKTOP Y MÓVIL) -->
      <section id="methodology" class="section-spacing">
        <div class="section-header centered-header">
          <span class="pill-tag">{{ t.methodologySection.badge }}</span>
          <h2>{{ t.methodologySection.title }}</h2>
          <p>{{ t.methodologySection.desc }}</p>
        </div>

        <div class="methodology-grid">
          <article
            v-for="(item, idx) in t.methodologySection.steps"
            :key="item.step"
            class="methodology-card"
          >
            <div class="methodology-card-top">
              <span class="methodology-step-badge">{{ item.step }}</span>
              <span class="methodology-step-num">0{{ idx + 1 }}</span>
            </div>
            <h3>{{ item.name }}</h3>
            <p>{{ item.detail }}</p>
          </article>
        </div>
      </section>

      <!-- 5. AUDITORÍA VIVA: CONTRASTE DE PROMPTS -->
      <section id="audit" class="section-spacing">
        <div class="section-header">
          <span class="pill-tag">{{ t.auditSection.badge }}</span>
          <h2>{{ t.auditSection.title }}</h2>
          <p>{{ t.auditSection.desc }}</p>
        </div>

        <div class="audit-comparison-grid">
          <article class="audit-card card-naive">
            <div class="audit-card-header">
              <span class="status-indicator warn" />
              <span class="audit-label">{{ t.auditSection.naiveLabel }}</span>
            </div>
            <blockquote class="audit-prompt-box">{{ t.auditSection.naivePrompt }}</blockquote>
            <p class="audit-verdict">{{ t.auditSection.naiveIssue }}</p>
          </article>

          <article class="audit-card card-verified">
            <div class="audit-card-header">
              <span class="status-indicator ok" />
              <span class="audit-label">{{ t.auditSection.parliaLabel }}</span>
            </div>
            <blockquote class="audit-prompt-box">{{ t.auditSection.parliaPrompt }}</blockquote>
            <p class="audit-verdict">{{ t.auditSection.parliaResult }}</p>
          </article>
        </div>
      </section>

      <!-- 6. IDENTIDAD UNIGUAJIRA Y TEJIDO KANAS WAYUU -->
      <section id="identity" class="section-spacing">
        <div class="vision-container">
          <div class="vision-left">
            <span class="pill-tag">{{ t.identitySection.badge }}</span>
            <h2>{{ t.identitySection.title }}</h2>
          </div>

          <div class="vision-right">
            <p>{{ t.identitySection.p1 }}</p>
            <p>{{ t.identitySection.p2 }}</p>
          </div>
        </div>

        <div class="demo-box">
          <div class="demo-overlay" />
          <div class="demo-content">
            <span class="pill-tag">{{ t.ctaBox.badge }}</span>
            <h3>{{ t.ctaBox.title }}</h3>
            <p>{{ t.ctaBox.desc }}</p>
            <div class="demo-actions">
              <button type="button" class="primary-button" @click="handleExplorePlatform">
                {{ authStore.isAuthenticated ? t.primaryCtaAuth : t.primaryCtaGuest }}
              </button>
              <router-link
                v-if="!authStore.isAuthenticated"
                to="/register"
                class="secondary-button"
              >
                {{ t.secondaryCtaGuest }}
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- 7. FOOTER -->
      <footer class="landing-footer">
        <div>ParLIA © 2026 · Universidad de La Guajira</div>
        <div>{{ t.footerCredits }}</div>
      </footer>
    </main>
  </div>
</template>

<style scoped>
.parlia-landing {
  --bg-deep: #050816;
  --card-glass: rgba(11, 18, 35, 0.72);
  --border-glass: rgba(255, 255, 255, 0.09);
  --text-light: #F3F4F6;
  --text-muted: #9CA3AF;
  --parlia-cyan: #20A4B8;
  --parlia-coral: #FF5B26;
  --parlia-ochre: #F99D1C;
  --parlia-gradient: linear-gradient(135deg, #FF5B26 0%, #F99D1C 100%);

  position: relative;
  min-height: 100vh;
  background-color: var(--bg-deep);
  color: var(--text-light);
  font-family: var(--font-family-base);
}

/* 1. VIDEO LOCAL Y GRILLA ESPACIAL DE FONDO */
.background-stage {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.background-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.4;
  filter: saturate(1.1) contrast(1.05);
}

.background-video-scrim {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 72% 42%,
    rgba(5, 8, 22, 0.42) 0%,
    rgba(5, 8, 22, 0.88) 76%
  );
}

.background-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.background-glow {
  position: absolute;
  width: 560px;
  height: 560px;
  border-radius: 50%;
  filter: blur(125px);
  opacity: 0.16;
}

.glow-cyan {
  background: var(--parlia-cyan);
  top: -180px;
  left: -180px;
}

.glow-coral {
  background: var(--parlia-coral);
  bottom: -220px;
  right: -220px;
}

/* 2. NAVBAR STICKY (TIPOGRAFÍA Y ESTÉTICA EJECUTIVA + MENÚ MÓVIL) */
.landing-navbar {
  position: sticky;
  top: 20px;
  width: min(1400px, 92%);
  margin: 0 auto;
  padding: 0.9rem 1.5rem;
  border: 1px solid var(--border-glass);
  background: rgba(10, 14, 30, 0.78);
  backdrop-filter: blur(20px);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  z-index: 50;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-light);
}

.brand-logo-img {
  width: 30px;
  height: 30px;
  object-fit: contain;
}

.brand-logo-text {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.brand-highlight {
  color: var(--parlia-coral);
}

.landing-nav-links {
  display: flex;
  align-items: center;
  gap: 1.8rem;
}

.landing-nav-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.25s ease;
}

.landing-nav-links a:hover {
  color: var(--text-light);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.lang-selector {
  display: flex;
  gap: 0.3rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 4px;
  border-radius: 10px;
  border: 1px solid var(--border-glass);
}

.lang-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 0.36rem 0.7rem;
  font-size: 0.8rem;
  font-weight: 600;
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.lang-btn.active {
  background: var(--parlia-gradient);
  color: #FFFFFF;
}

.nav-cta-button,
.primary-button,
.secondary-button {
  border: none;
  cursor: pointer;
  font-family: var(--font-family-base);
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.25s ease, filter 0.25s ease, border-color 0.25s ease;
}

.nav-cta-button,
.primary-button {
  background: var(--parlia-gradient);
  color: #FFFFFF;
}

.nav-cta-button {
  padding: 0.75rem 1.2rem;
  border-radius: 10px;
  font-size: 0.88rem;
}

.primary-button,
.secondary-button {
  padding: 0.95rem 1.5rem;
  border-radius: 12px;
  font-size: 0.96rem;
}

.secondary-button {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-glass);
  color: var(--text-light);
}

.primary-button:hover,
.nav-cta-button:hover {
  filter: brightness(1.08);
  color: #FFFFFF;
}

.secondary-button:hover {
  border-color: rgba(255, 255, 255, 0.3);
  color: #FFFFFF;
}

.mobile-menu-toggle {
  display: none;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-glass);
  color: var(--text-light);
  width: 38px;
  height: 38px;
  border-radius: 10px;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.mobile-nav-drawer {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  right: 0;
  background: rgba(8, 13, 28, 0.96);
  backdrop-filter: blur(22px);
  border: 1px solid var(--border-glass);
  border-radius: 14px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.95rem;
  z-index: 60;
}

.mobile-nav-drawer a {
  color: var(--text-light);
  text-decoration: none;
  font-size: 0.98rem;
  font-weight: 500;
  padding: 0.4rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.mobile-drawer-ctas {
  margin-top: 0.4rem;
}

.full-width {
  width: 100%;
}

/* CONTENEDOR PRINCIPAL */
.landing-main {
  width: min(1400px, 92%);
  margin: 0 auto;
  position: relative;
  z-index: 5;
}

/* 3. SECCIÓN HERO */
.hero-section {
  min-height: calc(100vh - 96px);
  display: flex;
  align-items: center;
  padding: 3rem 0;
}

.hero-left {
  max-width: 860px;
}

.pill-tag {
  display: inline-flex;
  padding: 0.5rem 0.95rem;
  border: 1px solid rgba(32, 164, 184, 0.38);
  background: rgba(32, 164, 184, 0.1);
  color: #7DD3FC;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.hero-display-title {
  font-size: clamp(2.65rem, 5.2vw, 4.9rem);
  font-weight: 800;
  line-height: 1.04;
  letter-spacing: -0.03em;
  color: #FFFFFF;
  margin-top: 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.12rem;
}

.title-accent-gradient {
  background: linear-gradient(90deg, #FF5B26 0%, #F99D1C 52%, #20A4B8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-description {
  margin-top: 1.6rem;
  max-width: 680px;
  color: var(--text-muted);
  line-height: 1.75;
  font-size: 1.06rem;
}

.hero-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2.2rem;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.15rem;
  margin-top: 2.8rem;
}

.stat-card,
.tech-card,
.methodology-card,
.demo-box,
.scroll-phase-card,
.audit-card {
  background: var(--card-glass);
  border: 1px solid var(--border-glass);
  backdrop-filter: blur(18px);
}

.stat-card {
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
}

.stat-card h3 {
  font-size: 1.35rem;
  color: #FFFFFF;
  margin-bottom: 0.3rem;
}

.stat-card span {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.45;
  display: block;
}

/* 4. ANIMACIÓN DE SCROLL CENTRAL Y GRANDE CON `para_animar.jpeg` */
.anime-scroll-track {
  position: relative;
  height: 280vh;
  margin: 2rem 0;
}

.anime-scroll-sticky {
  position: sticky;
  top: 86px;
  min-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.35rem;
  padding: 1rem 0;
}

.scroll-header-centered {
  text-align: center;
  max-width: 860px;
  margin: 0 auto;
}

.scroll-section-title {
  font-size: clamp(1.85rem, 3.2vw, 2.75rem);
  color: #FFFFFF;
  margin-top: 0.75rem;
  line-height: 1.12;
  letter-spacing: -0.02em;
}

.scroll-section-sub {
  color: var(--text-muted);
  max-width: 720px;
  margin: 0.5rem auto 0;
  font-size: 0.96rem;
  line-height: 1.6;
}

.scroll-stage-centered {
  width: 100%;
  max-width: 1120px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
}

.synapse-art-wrapper {
  position: relative;
  width: 100%;
  max-height: 54vh;
  aspect-ratio: 1000 / 700;
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(32, 164, 184, 0.35);
  background-color: #060D17;
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.62);
  will-change: transform;
  display: flex;
  align-items: center;
  justify-content: center;
}

.para-animar-dimmed {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  filter: brightness(0.38) saturate(0.65);
}

.synapse-spotlight-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  mask-image: radial-gradient(
    circle 390px at var(--spot-x, 20%) 50%,
    rgba(0, 0, 0, 1) 0%,
    rgba(0, 0, 0, 0.85) 55%,
    rgba(0, 0, 0, 0.15) 100%
  );
  -webkit-mask-image: radial-gradient(
    circle 390px at var(--spot-x, 20%) 50%,
    rgba(0, 0, 0, 1) 0%,
    rgba(0, 0, 0, 0.85) 55%,
    rgba(0, 0, 0, 0.15) 100%
  );
}

.para-animar-lit {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  filter: brightness(1.15) saturate(1.25) contrast(1.05);
}

.synapse-svg-overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 3;
}

/* Etiquetas HUD flotantes sobre el lienzo central */
.floating-hud {
  position: absolute;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  background: rgba(5, 8, 22, 0.84);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(10px);
  font-family: var(--font-family-mono);
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  opacity: 0.45;
  transform: translateY(6px);
  transition: opacity 0.35s ease, transform 0.35s ease, border-color 0.35s ease, color 0.35s ease;
}

.floating-hud.active {
  opacity: 1;
  color: #FFFFFF;
  transform: translateY(0);
  border-color: rgba(32, 164, 184, 0.55);
}

.hud-left {
  top: 16px;
  left: 18px;
}

.hud-center {
  bottom: 16px;
  left: 50%;
  transform: translate(-50%, 6px);
}

.hud-center.active {
  transform: translate(-50%, 0);
}

.hud-right {
  top: 16px;
  right: 18px;
}

.hud-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-ochre {
  background: var(--parlia-ochre);
  box-shadow: 0 0 8px var(--parlia-ochre);
}

.dot-coral {
  background: var(--parlia-coral);
  box-shadow: 0 0 8px var(--parlia-coral);
}

.dot-cyan {
  background: var(--parlia-cyan);
  box-shadow: 0 0 8px var(--parlia-cyan);
}

/* Fila de 3 Nodos centrada debajo de la imagen */
.scroll-phases-row {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.15rem;
}

.scroll-phase-card {
  padding: 1.15rem 1.35rem;
  border-radius: 16px;
  border-top: 3px solid rgba(255, 255, 255, 0.12);
  transition: border-color 0.3s ease, transform 0.3s ease, background-color 0.3s ease;
}

.scroll-phase-card.active {
  border-color: rgba(255, 91, 38, 0.45);
  border-top: 4px solid var(--parlia-coral);
  background: rgba(255, 91, 38, 0.1);
  transform: translateY(-4px);
}

.phase-step-code {
  font-family: var(--font-family-mono);
  font-size: 0.72rem;
  color: var(--parlia-ochre);
  font-weight: 700;
}

.scroll-phase-card h3 {
  color: #FFFFFF;
  font-size: 1.02rem;
  margin: 0.3rem 0;
}

.scroll-phase-card p {
  color: var(--text-muted);
  font-size: 0.84rem;
  margin: 0;
  line-height: 1.5;
}

/* 5. SECCIONES COMPLEMENTARIAS */
.section-spacing {
  padding: 6rem 0;
}

.section-header {
  max-width: 820px;
}

.centered-header {
  margin: 0 auto;
  text-align: center;
}

.section-header h2 {
  font-size: clamp(2rem, 4.2vw, 3.35rem);
  color: #FFFFFF;
  margin-top: 1.2rem;
  line-height: 1.12;
  letter-spacing: -0.02em;
}

.section-header p {
  margin-top: 1.1rem;
  color: var(--text-muted);
  line-height: 1.75;
  font-size: 1.02rem;
}

/* PILARES FORMATIVOS (4 DIMENSIONES EN GRILLA 2x2 BALANCEADA) */
.pillars-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.75rem;
  margin-top: 3rem;
}

.tech-card {
  padding: 2rem;
  border-radius: 20px;
  transition: transform 0.35s ease, border-color 0.35s ease;
}

.tech-card:hover {
  transform: translateY(-8px);
  border-color: rgba(32, 164, 184, 0.45);
}

.card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.95rem;
}

.card-number {
  font-family: var(--font-family-mono);
  color: var(--parlia-cyan);
  font-size: 0.95rem;
  font-weight: 700;
}

.card-badge-tag {
  font-family: var(--font-family-mono);
  font-size: 0.74rem;
  color: var(--parlia-ochre);
  background: rgba(249, 157, 28, 0.1);
  border: 1px solid rgba(249, 157, 28, 0.3);
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
}

.tech-card h3 {
  color: #FFFFFF;
  font-size: 1.28rem;
  margin-bottom: 0.75rem;
}

.tech-card p {
  color: var(--text-muted);
  line-height: 1.65;
  margin: 0;
}

/* METODOLOGÍA EN 4 ETAPAS: GRILLA DE 4 COLUMNAS IGUALES Y CENTRADAS EN DESKTOP */
.methodology-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-top: 3.2rem;
  align-items: stretch;
}

.methodology-card {
  padding: 1.85rem 1.6rem;
  border-radius: 20px;
  border-top: 3px solid var(--parlia-cyan);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  text-align: left;
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.methodology-card:nth-child(2) {
  border-top-color: var(--parlia-ochre);
}

.methodology-card:nth-child(3) {
  border-top-color: var(--parlia-coral);
}

.methodology-card:nth-child(4) {
  border-top-color: #10B981;
}

.methodology-card:hover {
  transform: translateY(-6px);
}

.methodology-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.methodology-step-badge {
  font-family: var(--font-family-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--parlia-cyan);
  letter-spacing: 0.06em;
}

.methodology-step-num {
  font-family: var(--font-family-mono);
  font-size: 1.35rem;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.14);
}

.methodology-card h3 {
  color: #FFFFFF;
  font-size: 1.16rem;
  margin-bottom: 0.65rem;
  line-height: 1.3;
}

.methodology-card p {
  color: var(--text-muted);
  font-size: 0.92rem;
  line-height: 1.6;
  margin: 0;
}

/* AUDITORÍA COMPARATIVA */
.audit-comparison-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.75rem;
  margin-top: 3rem;
}

.audit-card {
  padding: 2rem;
  border-radius: 20px;
}

.card-naive {
  border-left: 4px solid #EF4444;
}

.card-verified {
  border-left: 4px solid #10B981;
}

.audit-card-header {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 1.1rem;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-indicator.warn {
  background: #EF4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.6);
}

.status-indicator.ok {
  background: #10B981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
}

.audit-label {
  font-family: var(--font-family-mono);
  font-size: 0.78rem;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: 0.04em;
}

.audit-prompt-box {
  margin: 0 0 1.2rem;
  padding: 1.1rem 1.25rem;
  border-radius: 12px;
  background: rgba(5, 8, 22, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.07);
  font-family: var(--font-family-mono);
  font-size: 0.86rem;
  color: #E2E8F0;
  line-height: 1.65;
}

.audit-verdict {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.92rem;
  line-height: 1.6;
}

/* IDENTIDAD Y CAJA CTA */
.vision-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3.5rem;
  align-items: start;
}

.vision-left h2 {
  font-size: clamp(2rem, 4vw, 3.2rem);
  color: #FFFFFF;
  margin-top: 1.2rem;
  line-height: 1.12;
}

.vision-right p {
  color: var(--text-muted);
  line-height: 1.85;
  margin-bottom: 1.5rem;
  font-size: 1.04rem;
}

.demo-box {
  position: relative;
  margin-top: 3.5rem;
  border-radius: 24px;
  overflow: hidden;
  padding: 3rem;
}

.demo-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at 70% 35%,
    rgba(32, 164, 184, 0.22),
    rgba(255, 91, 38, 0.1) 45%,
    transparent 72%
  );
  pointer-events: none;
}

.demo-content {
  position: relative;
  z-index: 2;
  max-width: 680px;
}

.demo-content h3 {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  color: #FFFFFF;
  margin: 1rem 0 0.75rem;
}

.demo-content p {
  color: var(--text-muted);
  margin-bottom: 1.75rem;
  line-height: 1.7;
}

.demo-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

/* FOOTER */
.landing-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 2.8rem 0;
  border-top: 1px solid var(--border-glass);
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* RESPONSIVIDAD TABLET Y MÓVIL */
@media (max-width: 1120px) {
  .methodology-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .scroll-phases-row {
    grid-template-columns: 1fr;
  }

  .synapse-art-wrapper {
    max-height: none;
  }
}

@media (max-width: 960px) {
  .vision-container,
  .pillars-grid,
  .audit-comparison-grid,
  .hero-stats {
    grid-template-columns: 1fr;
  }

  .anime-scroll-track {
    height: 220vh;
  }

  .anime-scroll-sticky {
    top: 82px;
  }
}

@media (max-width: 768px) {
  .landing-navbar {
    top: 12px;
    padding: 0.75rem 1rem;
  }

  .landing-nav-links,
  .desktop-only-btn {
    display: none;
  }

  .mobile-menu-toggle {
    display: inline-flex;
  }

  .hero-section {
    min-height: auto;
    padding: 2.5rem 0 2rem;
  }

  .hero-display-title {
    font-size: clamp(2.15rem, 8.5vw, 3rem);
  }

  .hero-buttons {
    flex-direction: column;
  }

  .hero-buttons .primary-button,
  .hero-buttons .secondary-button {
    width: 100%;
  }

  .anime-scroll-track {
    height: 210vh;
  }

  .anime-scroll-sticky {
    top: 74px;
    justify-content: flex-start;
    gap: 1rem;
  }

  .floating-hud {
    font-size: 0.58rem;
    padding: 0.25rem 0.55rem;
  }

  .hud-center {
    display: none;
  }

  .methodology-grid {
    grid-template-columns: 1fr;
  }

  .section-spacing {
    padding: 4rem 0;
  }

  .demo-box {
    padding: 1.85rem 1.4rem;
  }

  .demo-actions {
    flex-direction: column;
  }

  .demo-actions .primary-button,
  .demo-actions .secondary-button {
    width: 100%;
  }
}
</style>
