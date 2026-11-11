<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import anime from 'animejs/lib/anime.es.js'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const currentLang = ref(localStorage.getItem('parlia_lang') || 'ES')
const activeSection = ref('technology')
const isotypeSvgRef = ref(null)

// Video oficial de fondo provisto por el usuario: https://youtu.be/gEEKKXmLTIA
const YOUTUBE_VIDEO_ID = 'gEEKKXmLTIA'
const youtubeEmbedUrl = `https://www.youtube.com/embed/${YOUTUBE_VIDEO_ID}?autoplay=1&mute=1&loop=1&playlist=${YOUTUBE_VIDEO_ID}&controls=0&showinfo=0&rel=0&modestbranding=1&iv_load_policy=3&disablekb=1&playsinline=1`

const translations = {
  ES: {
    nav: [
      { id: 'technology', label: 'Tecnología' },
      { id: 'system', label: 'Sistema' },
      { id: 'vision', label: 'Visión' },
      { id: 'methodology', label: 'Metodología' },
      { id: 'horizon', label: 'Horizonte' },
    ],
    explorePlatform: 'Explorar Plataforma',
    headlineLine1: 'Domina la IA',
    headlineLine2: 'Generativa con',
    headlineLine3: 'Criterio en',
    headlineLine4: 'Ingeniería.',
    description:
      'Un laboratorio virtual de aprendizaje reflexivo y no punitivo capaz de transformar la interacción empírica con modelos de lenguaje en ingeniería de prompts estructurada, verificación algorítmica y ética profesional.',
    primaryCtaGuest: 'Iniciar Sesión',
    secondaryCtaGuest: 'Crear Cuenta',
    primaryCtaAuth: 'Ir a Mis Módulos',
    secondaryCtaAuth: 'Ver Mi Progreso',
  },
  EN: {
    nav: [
      { id: 'technology', label: 'Technology' },
      { id: 'system', label: 'System' },
      { id: 'vision', label: 'Vision' },
      { id: 'methodology', label: 'Methodology' },
      { id: 'horizon', label: 'Horizon' },
    ],
    explorePlatform: 'Explore Platform',
    headlineLine1: 'Master',
    headlineLine2: 'Generative AI',
    headlineLine3: 'Beyond',
    headlineLine4: 'Prompts.',
    description:
      'A non-punitive virtual learning laboratory capable of transforming empirical AI interaction into structured prompt engineering, algorithmic verification, and professional engineering judgment.',
    primaryCtaGuest: 'Sign In',
    secondaryCtaGuest: 'Create Account',
    primaryCtaAuth: 'Go to Modules',
    secondaryCtaAuth: 'View My Progress',
  },
}

const t = computed(() => translations[currentLang.value] || translations.ES)

function setLanguage(lang) {
  currentLang.value = lang
  localStorage.setItem('parlia_lang', lang)
}

function handleExploreClick() {
  if (authStore.isAuthenticated) {
    router.push('/modules')
  } else {
    router.push('/login')
  }
}

function animateVisualstage() {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced || !isotypeSvgRef.value) return

  const paths = isotypeSvgRef.value.querySelectorAll('.wayuu-line')
  paths.forEach((p) => {
    const len = p.getTotalLength ? p.getTotalLength() : 320
    p.style.strokeDasharray = `${len}`
    p.style.strokeDashoffset = `${len}`
  })

  anime({
    targets: paths,
    strokeDashoffset: [anime.setDashoffset, 0],
    easing: 'easeInOutSine',
    duration: 2200,
    delay: anime.stagger(110),
  })

  anime({
    targets: isotypeSvgRef.value.querySelectorAll('.matrix-tile'),
    opacity: [0.18, 0.72, 0.28],
    easing: 'easeInOutSine',
    duration: 2800,
    delay: anime.stagger(140, { grid: [4, 4], from: 'center' }),
    loop: true,
    direction: 'alternate',
  })

  anime({
    targets: isotypeSvgRef.value.querySelectorAll('.wayuu-node'),
    scale: [0.85, 1.18, 1],
    opacity: [0.5, 1],
    easing: 'easeInOutQuad',
    duration: 2000,
    delay: anime.stagger(120),
    loop: true,
    direction: 'alternate',
  })
}

onMounted(() => {
  animateVisualstage()
})
</script>

<template>
  <div class="voxel-stage">
    <!-- 1. VIDEO DE FONDO A PANTALLA COMPLETA + REJILLA ESPACIAL PROFUNDA -->
    <div class="stage-background" aria-hidden="true">
      <iframe
        class="stage-video"
        :src="youtubeEmbedUrl"
        title="ParLIA Cinematic Background"
        frameborder="0"
        allow="autoplay; encrypted-media"
        tabindex="-1"
      />
      <div class="stage-gradient-overlay" />
      <div class="stage-perspective-grid" />
    </div>

    <!-- 2. BARRA SUPERIOR FLOTANTE (ESTILO VOXEL) -->
    <header class="voxel-navbar">
      <router-link to="/" class="voxel-brand">
        <img
          src="/logo_parlia.png"
          alt="Isotipo ParLIA"
          class="voxel-brand-icon"
        />
        <span class="voxel-brand-name">
          Par<span class="accent-lia">LIA</span>
        </span>
      </router-link>

      <nav class="voxel-center-links" aria-label="Conceptos del sistema">
        <button
          v-for="item in t.nav"
          :key="item.id"
          type="button"
          class="voxel-nav-btn"
          :class="{ active: activeSection === item.id }"
          @click="activeSection = item.id"
        >
          {{ item.label }}
        </button>
      </nav>

      <div class="voxel-right-controls">
        <div class="lang-pill" role="group" aria-label="Selector de idioma">
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

        <button
          type="button"
          class="explore-cta-btn"
          @click="handleExploreClick"
        >
          {{ t.explorePlatform }}
        </button>
      </div>
    </header>

    <!-- 3. LIENZO CENTRAL INMERSIVO (SIN MÓDULOS NI CARRERAS ANTES DE INICIAR SESIÓN) -->
    <main class="voxel-hero-main">
      <!-- Columna Izquierda: Tipografía de Alto Impacto + Descripción + 2 Botones -->
      <div class="voxel-hero-left">
        <h1 class="voxel-display-title">
          <span>{{ t.headlineLine1 }}</span>
          <span>{{ t.headlineLine2 }}</span>
          <span>{{ t.headlineLine3 }}</span>
          <span>{{ t.headlineLine4 }}</span>
        </h1>

        <p class="voxel-lead">
          {{ t.description }}
        </p>

        <div class="voxel-action-row">
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="voxel-btn-primary">
              {{ t.primaryCtaGuest }}
            </router-link>
            <router-link to="/register" class="voxel-btn-ghost">
              {{ t.secondaryCtaGuest }}
            </router-link>
          </template>

          <template v-else>
            <router-link to="/modules" class="voxel-btn-primary">
              {{ t.primaryCtaAuth }}
            </router-link>
            <router-link to="/progress" class="voxel-btn-ghost">
              {{ t.secondaryCtaAuth }}
            </router-link>
          </template>
        </div>
      </div>

      <!-- Columna Derecha: Matriz Volumétrica Isométrica + Isotipo Kanas Wayuu ParLIA -->
      <div class="voxel-hero-right" aria-hidden="true">
        <svg
          ref="isotypeSvgRef"
          viewBox="0 0 560 460"
          class="voxel-holo-svg"
        >
          <defs>
            <radialGradient id="holoGlow" cx="50%" cy="55%" r="50%">
              <stop offset="0%" stop-color="#20A4B8" stop-opacity="0.38" />
              <stop offset="45%" stop-color="#FF5B26" stop-opacity="0.14" />
              <stop offset="100%" stop-color="#050814" stop-opacity="0" />
            </radialGradient>

            <linearGradient id="tileStroke" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#20A4B8" stop-opacity="0.85" />
              <stop offset="100%" stop-color="#FF5B26" stop-opacity="0.65" />
            </linearGradient>
          </defs>

          <!-- Halo volumétrico inferior -->
          <ellipse cx="290" cy="295" rx="220" ry="110" fill="url(#holoGlow)" />

          <!-- Matriz Isométrica de Celdas (Inspirada en la referencia Voxel) -->
          <g transform="translate(290, 295) scale(1, 0.54) rotate(45)">
            <g transform="translate(-140, -140)">
              <rect class="matrix-tile" x="0" y="0" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="72" y="0" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="144" y="0" width="56" height="56" rx="6" fill="#13294B" stroke="#20A4B8" stroke-width="2.5" />
              <rect class="matrix-tile" x="216" y="0" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />

              <rect class="matrix-tile" x="0" y="72" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="72" y="72" width="56" height="56" rx="6" fill="#162F54" stroke="#FF5B26" stroke-width="2.5" />
              <rect class="matrix-tile" x="144" y="72" width="56" height="56" rx="6" fill="#162F54" stroke="#F99D1C" stroke-width="2.5" />
              <rect class="matrix-tile" x="216" y="72" width="56" height="56" rx="6" fill="#13294B" stroke="#20A4B8" stroke-width="2.5" />

              <rect class="matrix-tile" x="0" y="144" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="72" y="144" width="56" height="56" rx="6" fill="#162F54" stroke="#20A4B8" stroke-width="2.5" />
              <rect class="matrix-tile" x="144" y="144" width="56" height="56" rx="6" fill="#1D3B68" stroke="#FF5B26" stroke-width="2.5" />
              <rect class="matrix-tile" x="216" y="144" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />

              <rect class="matrix-tile" x="0" y="216" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="72" y="216" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="144" y="216" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
              <rect class="matrix-tile" x="216" y="216" width="56" height="56" rx="6" fill="#0F1E36" stroke="url(#tileStroke)" stroke-width="2" />
            </g>
          </g>

          <!-- Isotipo Holográfico ParLIA suspendido sobre la matriz -->
          <g transform="translate(175, 45) scale(0.88)">
            <path
              class="wayuu-line"
              d="M 28 130 A 102 102 0 0 1 232 130"
              fill="none"
              stroke="#F99D1C"
              stroke-width="5"
              stroke-linecap="round"
            />
            <path
              class="wayuu-line"
              d="M 28 130 A 102 102 0 0 0 232 130"
              fill="none"
              stroke="#20A4B8"
              stroke-width="5"
              stroke-linecap="round"
            />
            <polygon
              class="wayuu-line"
              points="130,36 224,130 130,224 36,130"
              fill="none"
              stroke="#FF5B26"
              stroke-width="5"
              stroke-linejoin="round"
            />
            <polygon
              class="wayuu-line"
              points="130,92 168,130 130,168 92,130"
              fill="none"
              stroke="#20A4B8"
              stroke-width="4.5"
            />
            <polygon
              class="wayuu-line"
              points="130,110 150,130 130,150 110,130"
              fill="none"
              stroke="#FF5B26"
              stroke-width="4"
            />

            <circle class="wayuu-node" cx="130" cy="28" r="7" fill="#F99D1C" />
            <circle class="wayuu-node" cx="232" cy="130" r="7" fill="#FF5B26" />
            <circle class="wayuu-node" cx="130" cy="232" r="7" fill="#20A4B8" />
            <circle class="wayuu-node" cx="28" cy="130" r="7" fill="#FF5B26" />
          </g>
        </svg>
      </div>
    </main>
  </div>
</template>

<style scoped>
.voxel-stage {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background-color: #050711;
  color: #FFFFFF;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 32px 40px;
}

/* 1. FONDO CINEMÁTICO + GRID VOLUMÉTRICO */
.stage-background {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.stage-video {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 177.78vh;
  min-width: 100%;
  height: 56.25vw;
  min-height: 100%;
  transform: translate(-50%, -50%) scale(1.1);
  opacity: 0.34;
  filter: saturate(1.1) contrast(1.08);
}

.stage-gradient-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 72% 62%, rgba(32, 164, 184, 0.16) 0%, transparent 48%),
    radial-gradient(circle at 20% 30%, rgba(12, 30, 47, 0.72) 0%, rgba(5, 7, 17, 0.92) 78%);
}

.stage-perspective-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse at center, black 35%, transparent 85%);
}

/* 2. NAVBAR FLOTANTE OSCURA (ESTILO VOXEL) */
.voxel-navbar {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1360px;
  margin: 0 auto;
  height: 64px;
  padding: 0 22px;
  border-radius: 10px;
  background-color: rgba(11, 15, 28, 0.78);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.voxel-brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #FFFFFF;
  text-decoration: none;
}

.voxel-brand-icon {
  width: 30px;
  height: 30px;
  object-fit: contain;
}

.voxel-brand-name {
  font-size: 1.12rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: #FFFFFF;
}

.accent-lia {
  color: #FF5B26;
}

.voxel-center-links {
  display: flex;
  align-items: center;
  gap: 28px;
}

.voxel-nav-btn {
  background: transparent;
  border: none;
  color: #94A3B8;
  font-family: var(--font-family-base);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 180ms ease;
}

.voxel-nav-btn:hover,
.voxel-nav-btn.active {
  color: #F8FAFC;
}

.voxel-right-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}

.lang-pill {
  display: inline-flex;
  align-items: center;
  padding: 3px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.lang-btn {
  border: none;
  background: transparent;
  color: #94A3B8;
  font-family: var(--font-family-base);
  font-size: 0.76rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 180ms ease, color 180ms ease;
}

.lang-btn.active {
  background-color: #20A4B8;
  color: #FFFFFF;
}

.explore-cta-btn {
  padding: 9px 18px;
  border-radius: 8px;
  border: 1px solid rgba(255, 91, 38, 0.5);
  background: linear-gradient(135deg, #FF5B26 0%, #F99D1C 100%);
  color: #FFFFFF;
  font-family: var(--font-family-base);
  font-size: 0.86rem;
  font-weight: 600;
  cursor: pointer;
  transition: filter 180ms ease, transform 180ms ease;
}

.explore-cta-btn:hover {
  filter: brightness(1.08);
}

/* 3. ESCENARIO CENTRAL HERO */
.voxel-hero-main {
  position: relative;
  z-index: 5;
  width: 100%;
  max-width: 1320px;
  margin: auto;
  padding: 32px 12px;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
  align-items: center;
  gap: 40px;
}

.voxel-display-title {
  display: flex;
  flex-direction: column;
  font-size: clamp(2.85rem, 5.6vw, 5.1rem);
  font-weight: 700;
  line-height: 1.04;
  letter-spacing: -0.035em;
  color: #FFFFFF;
  margin-bottom: 28px;
}

.voxel-lead {
  color: #94A3B8;
  font-size: clamp(0.96rem, 1.15vw, 1.08rem);
  line-height: 1.65;
  max-width: 540px;
  margin-bottom: 36px;
}

.voxel-action-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.voxel-btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 156px;
  height: 48px;
  padding: 0 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, #FF5B26 0%, #F99D1C 100%);
  color: #FFFFFF;
  font-size: 0.92rem;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 8px 24px rgba(255, 91, 38, 0.25);
  transition: filter 180ms ease;
}

.voxel-btn-primary:hover {
  color: #FFFFFF;
  filter: brightness(1.08);
}

.voxel-btn-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 168px;
  height: 48px;
  padding: 0 24px;
  border-radius: 8px;
  background-color: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.14);
  color: #F8FAFC;
  font-size: 0.92rem;
  font-weight: 600;
  text-decoration: none;
  transition: border-color 180ms ease, background-color 180ms ease;
}

.voxel-btn-ghost:hover {
  color: #FFFFFF;
  border-color: rgba(255, 255, 255, 0.36);
  background-color: rgba(30, 41, 59, 0.85);
}

.voxel-hero-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.voxel-holo-svg {
  width: 100%;
  max-width: 540px;
  height: auto;
}

@media (max-width: 960px) {
  .voxel-stage {
    padding: 16px 18px 32px;
  }

  .voxel-center-links {
    display: none;
  }

  .voxel-hero-main {
    grid-template-columns: 1fr;
    padding-top: 28px;
  }
}
</style>
