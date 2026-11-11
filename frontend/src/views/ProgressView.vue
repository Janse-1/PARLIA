<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import anime from 'animejs/lib/anime.es.js'
import { useProgressStore } from '../stores/progress'

const router = useRouter()
const progressStore = useProgressStore()

const pathSvgRef = ref(null)
const progressPathRef = ref(null)
const warriorGroupRef = ref(null)
const selectedOrder = ref(null)
const isWalking = ref(false)
const warriorFacingLeft = ref(false)

// Coordenadas exactas sobre la ladera y escalera serpenteante de la montaña (viewBox 0 0 900 1020)
// Ordenadas de abajo (Campamento 1) hacia la Cumbre (Campamento 6 / Meta)
const campNodes = [
  {
    order: 1,
    x: 330,
    y: 880,
    labelSide: 'left',
    defaultTitle: 'Fundamentos de la Inteligencia Artificial Generativa',
    subtitle: 'Campamento Base: Predicción de tokens y arquitectura LLM',
  },
  {
    order: 2,
    x: 545,
    y: 745,
    labelSide: 'right',
    defaultTitle: 'Ingeniería de Prompts',
    subtitle: 'Terraza 2: Estructura técnica, rol y razonamiento',
  },
  {
    order: 3,
    x: 350,
    y: 610,
    labelSide: 'left',
    defaultTitle: 'Verificaciones',
    subtitle: 'Mirador 3: Detección de alucinaciones y auditoría',
  },
  {
    order: 4,
    x: 615,
    y: 480,
    labelSide: 'right',
    defaultTitle: 'Ética, Privacidad e Integridad Académica',
    subtitle: 'Balcón 4: Transparencia y resguardo de datos',
  },
  {
    order: 5,
    x: 385,
    y: 355,
    labelSide: 'left',
    defaultTitle: 'Aplicación en investigación, redacción',
    subtitle: 'Campamento Alto 5: Síntesis con voz analítica propia',
  },
  {
    order: 6,
    x: 535,
    y: 230,
    labelSide: 'right',
    defaultTitle: 'Actividades finales',
    subtitle: 'Antesala de la Cumbre: Reto integrador de ingeniería',
  },
]

const summitCoords = { x: 495, y: 120 }

// Trazado continuo que pasa exactamente por cada campamento y llega a la cumbre
const mountainPathD =
  'M 330 880 C 430 840, 470 790, 545 745 C 500 685, 410 655, 350 610 C 430 560, 535 530, 615 480 C 535 430, 450 400, 385 355 C 445 305, 495 270, 535 230 C 520 185, 505 155, 495 120'

// Peldaños tallados en la montaña a lo largo del sendero
const stairSteps = [
  { x: 330, y: 880, w: 72 },
  { x: 375, y: 852, w: 52 },
  { x: 422, y: 824, w: 52 },
  { x: 468, y: 796, w: 52 },
  { x: 510, y: 770, w: 54 },
  { x: 545, y: 745, w: 76 },
  { x: 505, y: 716, w: 50 },
  { x: 462, y: 688, w: 50 },
  { x: 420, y: 660, w: 50 },
  { x: 382, y: 634, w: 52 },
  { x: 350, y: 610, w: 76 },
  { x: 405, y: 582, w: 52 },
  { x: 462, y: 554, w: 52 },
  { x: 518, y: 528, w: 52 },
  { x: 570, y: 502, w: 54 },
  { x: 615, y: 480, w: 78 },
  { x: 565, y: 452, w: 50 },
  { x: 515, y: 425, w: 50 },
  { x: 468, y: 400, w: 50 },
  { x: 424, y: 376, w: 50 },
  { x: 385, y: 355, w: 74 },
  { x: 425, y: 326, w: 46 },
  { x: 465, y: 295, w: 46 },
  { x: 502, y: 262, w: 46 },
  { x: 535, y: 230, w: 68 },
  { x: 522, y: 198, w: 42 },
  { x: 510, y: 166, w: 38 },
  { x: 495, y: 125, w: 56 },
]

const enrichedCamps = computed(() => {
  const byOrder = {}
  for (const m of progressStore.modules) {
    byOrder[m.order] = m
  }
  return campNodes.map((node) => {
    const apiMod = byOrder[node.order]
    return {
      ...node,
      module_id: apiMod?.module_id || node.order,
      title: apiMod?.title || node.defaultTitle,
      status: apiMod?.status || 'pending',
      percentage: apiMod?.percentage || 0,
      completed_lessons: apiMod?.completed_lessons || 0,
      total_lessons: apiMod?.total_lessons || 1,
    }
  })
})

// Determina la estación actual real según el progreso en MySQL
const activeProgressOrder = computed(() => {
  const camps = enrichedCamps.value
  const allCompleted = camps.length > 0 && camps.every((c) => c.status === 'completed')
  if (allCompleted) return 7 // Cumbre alcanzada

  const inProg = camps.find((c) => c.status === 'in_progress')
  if (inProg) return inProg.order

  let lastCompletedOrder = 0
  for (const c of camps) {
    if (c.status === 'completed') lastCompletedOrder = c.order
  }
  return Math.min(6, lastCompletedOrder + 1)
})

const selectedCamp = computed(() => {
  const targetOrder = selectedOrder.value || Math.min(6, activeProgressOrder.value)
  return enrichedCamps.value.find((c) => c.order === targetOrder) || enrichedCamps.value[0]
})

function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

// Obtiene la longitud acumulada sobre el path SVG hasta un punto (x, y)
function getLengthAtPoint(svgPath, targetX, targetY) {
  const totalLen = svgPath.getTotalLength()
  let bestLen = 0
  let minDist = Infinity
  const samples = 280
  for (let i = 0; i <= samples; i++) {
    const len = (i / samples) * totalLen
    const pt = svgPath.getPointAtLength(len)
    const dist = Math.hypot(pt.x - targetX, pt.y - targetY)
    if (dist < minDist) {
      minDist = dist
      bestLen = len
    }
  }
  return { length: bestLen, totalLength: totalLen }
}

let currentWarriorLength = 0
let currentWalkAnimation = null

function animatePathAndWarrior(targetOrder, immediate = false) {
  const svgPath = progressPathRef.value
  const warriorEl = warriorGroupRef.value
  if (!svgPath || !warriorEl) return

  const targetCoords =
    targetOrder >= 7
      ? summitCoords
      : campNodes.find((c) => c.order === targetOrder) || campNodes[0]

  const { length: targetLen, totalLength } = getLengthAtPoint(
    svgPath,
    targetCoords.x,
    targetCoords.y
  )

  // Trazar camino recorrido según el progreso real del estudiante
  const realTargetCoords =
    activeProgressOrder.value >= 7
      ? summitCoords
      : campNodes.find((c) => c.order === activeProgressOrder.value) || campNodes[0]
  const { length: realLen } = getLengthAtPoint(
    svgPath,
    realTargetCoords.x,
    realTargetCoords.y
  )

  svgPath.style.strokeDasharray = `${totalLength}`

  if (immediate || prefersReducedMotion()) {
    svgPath.style.strokeDashoffset = `${totalLength - realLen}`
    const pt = svgPath.getPointAtLength(targetLen)
    warriorEl.setAttribute('transform', `translate(${pt.x}, ${pt.y})`)
    currentWarriorLength = targetLen
    isWalking.value = false
    return
  }

  // 1. Animación del trazo del sendero con Anime.js (DESING.md 5.2)
  anime({
    targets: svgPath,
    strokeDashoffset: [totalLength, totalLength - realLen],
    easing: 'easeInOutSine',
    duration: 1400,
  })

  // 2. Animación del guerrero caminando paso a paso por la curva del sendero
  if (currentWalkAnimation) currentWalkAnimation.pause()

  const tracker = { dist: currentWarriorLength }
  isWalking.value = Math.abs(targetLen - currentWarriorLength) > 4

  currentWalkAnimation = anime({
    targets: tracker,
    dist: targetLen,
    duration: 1650,
    easing: 'easeInOutQuad',
    update() {
      const pt = svgPath.getPointAtLength(tracker.dist)
      const ahead = svgPath.getPointAtLength(Math.min(totalLength, tracker.dist + 4))
      warriorFacingLeft.value = ahead.x < pt.x - 0.3
      // Pequeño rebote rítmico de caminata al subir escalones
      const stepBounce = isWalking.value ? Math.abs(Math.sin(tracker.dist * 0.18)) * -5 : 0
      warriorEl.setAttribute('transform', `translate(${pt.x}, ${pt.y + stepBounce})`)
    },
    complete() {
      currentWarriorLength = targetLen
      isWalking.value = false
      const finalPt = svgPath.getPointAtLength(targetLen)
      warriorEl.setAttribute('transform', `translate(${finalPt.x}, ${finalPt.y})`)
    },
  })
}

function selectCamp(camp) {
  selectedOrder.value = camp.order
  animatePathAndWarrior(camp.order, false)
}

function goToModule(moduleId) {
  router.push(`/modules/${moduleId}`)
}

onMounted(async () => {
  try {
    await progressStore.fetchMyProgress()
  } catch {
    // Manejado por store
  }
  await nextTick()
  selectedOrder.value = Math.min(6, activeProgressOrder.value)
  animatePathAndWarrior(activeProgressOrder.value, false)
})

watch(activeProgressOrder, (newOrder) => {
  selectedOrder.value = Math.min(6, newOrder)
  animatePathAndWarrior(newOrder, false)
})
</script>

<template>
  <section class="expedition-view">
    <header class="expedition-header">
      <div>
        <span class="badge badge-primary">Ruta Interactiva de Progreso</span>
        <h1>La Expedición del Guerrero a la Montaña</h1>
        <p class="subtitle">
          Haz clic en cualquier campamento de la montaña para desplazar al explorador e inspeccionar tu avance hacia la Cumbre del Criterio Técnico.
        </p>
      </div>

      <div class="summary-pill card">
        <div class="summary-stat">
          <span class="stat-label">Avance Global</span>
          <strong class="stat-value">{{ progressStore.overallPercentage }}%</strong>
        </div>
        <div class="summary-divider" />
        <div class="summary-stat">
          <span class="stat-label">Lecciones Superadas</span>
          <strong class="stat-value">
            {{ progressStore.completedLessons }} / {{ progressStore.totalLessons }}
          </strong>
        </div>
      </div>
    </header>

    <div class="expedition-layout">
      <!-- Lienzo Ilustrado e Interactivo de la Montaña -->
      <div class="card mountain-canvas-card">
        <svg
          ref="pathSvgRef"
          viewBox="0 0 900 1020"
          class="mountain-svg"
          role="img"
          aria-label="Mapa interactivo de ascenso a la montaña PARLIA con 6 campamentos"
        >
          <defs>
            <!-- Gradiente del cielo estilo atardecer/amanecer alpino -->
            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#3B8296" />
              <stop offset="32%" stop-color="#84C0C6" />
              <stop offset="68%" stop-color="#F6D5B0" />
              <stop offset="100%" stop-color="#F7B28B" />
            </linearGradient>

            <!-- Resplandor del Sol Dorado en la Cumbre -->
            <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#FFFBEB" stop-opacity="1" />
              <stop offset="35%" stop-color="#FDDA24" stop-opacity="0.85" />
              <stop offset="70%" stop-color="#E76F51" stop-opacity="0.3" />
              <stop offset="100%" stop-color="#E76F51" stop-opacity="0" />
            </radialGradient>

            <!-- Cara iluminada de la montaña (Izquierda) -->
            <linearGradient id="mountainLit" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#FFFDF7" />
              <stop offset="28%" stop-color="#F6D6AD" />
              <stop offset="65%" stop-color="#C88A78" />
              <stop offset="100%" stop-color="#7C5869" />
            </linearGradient>

            <!-- Cara en sombra de la montaña (Derecha) -->
            <linearGradient id="mountainShadow" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#B9C8D8" />
              <stop offset="35%" stop-color="#5E7394" />
              <stop offset="75%" stop-color="#3D4C6B" />
              <stop offset="100%" stop-color="#283149" />
            </linearGradient>

            <!-- Gradiente de los escalones dorados -->
            <linearGradient id="stairGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#FDE68A" />
              <stop offset="60%" stop-color="#D99B43" />
              <stop offset="100%" stop-color="#9E671E" />
            </linearGradient>
          </defs>

          <!-- 1. Fondo de Cielo -->
          <rect width="900" height="1020" rx="12" fill="url(#skyGrad)" />

          <!-- 2. Arcoíris sutil en el horizonte izquierdo -->
          <g opacity="0.55">
            <path d="M 110 530 A 130 130 0 0 1 370 530" fill="none" stroke="#E76F51" stroke-width="8" />
            <path d="M 118 530 A 122 122 0 0 1 362 530" fill="none" stroke="#FDDA24" stroke-width="8" />
            <path d="M 126 530 A 114 114 0 0 1 354 530" fill="none" stroke="#2A9D8F" stroke-width="8" />
          </g>

          <!-- 3. Nubes de fondo y aves vectoriales animadas -->
          <g class="ambient-clouds" opacity="0.75">
            <path
              d="M 80 280 Q 110 250 145 268 Q 175 240 215 265 Q 245 260 255 285 L 70 285 Z"
              fill="#FDE8D0"
            />
            <path
              d="M 670 220 Q 700 192 735 208 Q 768 188 798 215 L 660 215 Z"
              fill="#FDE8D0"
            />
          </g>

          <!-- Aves en vuelo hacia la cumbre -->
          <g class="sky-birds" stroke="#FFFDF9" stroke-width="2.2" fill="none" stroke-linecap="round">
            <path class="bird bird-1" d="M 210 150 Q 220 140 230 150 Q 240 140 250 150" />
            <path class="bird bird-2" d="M 330 110 Q 338 102 346 110 Q 354 102 362 110" />
            <path class="bird bird-3" d="M 690 135 Q 700 124 710 135 Q 720 124 730 135" />
          </g>

          <!-- 4. El Sol Dorado en la Cumbre -->
          <g class="summit-sun">
            <circle cx="495" cy="115" r="115" fill="url(#sunGlow)" class="sun-pulse" />
            <circle cx="495" cy="115" r="46" fill="#FFFBEB" />
          </g>

          <!-- 5. Montañas secundarias lejanas -->
          <polygon points="40,780 155,560 285,780" fill="#5E788D" opacity="0.55" />
          <polygon points="640,760 775,540 885,760" fill="#4B5D78" opacity="0.6" />

          <!-- 6. La Gran Montaña Principal (Polígonos facetados estilo ilustración) -->
          <!-- Cara iluminada izquierda -->
          <polygon
            points="495,115 85,960 465,960"
            fill="url(#mountainLit)"
          />
          <!-- Cara en sombra derecha -->
          <polygon
            points="495,115 465,960 855,960"
            fill="url(#mountainShadow)"
          />
          <!-- Pliegues de roca y aristas de nieve en la cumbre -->
          <polygon
            points="495,115 415,310 475,285 495,190 538,295 570,265"
            fill="#FFFDF9"
            opacity="0.88"
          />
          <polygon
            points="495,115 465,960 520,620 480,420"
            fill="#32415C"
            opacity="0.38"
          />

          <!-- 7. Peldaños de la Escalera Serpenteante -->
          <g class="mountain-stairs">
            <g v-for="(step, idx) in stairSteps" :key="idx">
              <rect
                :x="step.x - step.w / 2"
                :y="step.y - 5"
                :width="step.w"
                height="9"
                rx="2"
                fill="url(#stairGrad)"
              />
              <rect
                :x="step.x - step.w / 2"
                :y="step.y + 4"
                :width="step.w"
                height="5"
                fill="#7C4D15"
                opacity="0.75"
              />
            </g>
          </g>

          <!-- 8. Sendero Pendiente (Gris Punteado #D1D5DB) -->
          <path
            :d="mountainPathD"
            fill="none"
            stroke="#D1D5DB"
            stroke-width="6"
            stroke-dasharray="10 10"
            stroke-linecap="round"
          />

          <!-- 9. Sendero Completado / Activo (Aguamarina Caribe #2A9D8F) -->
          <path
            id="path-progress"
            ref="progressPathRef"
            :d="mountainPathD"
            fill="none"
            stroke="#2A9D8F"
            stroke-width="7"
            stroke-linecap="round"
          />

          <!-- 10. Meta en la Cumbre -->
          <g
            class="summit-goal"
            :transform="`translate(${summitCoords.x}, ${summitCoords.y})`"
          >
            <circle r="14" fill="#C2822B" stroke="#FFFBEB" stroke-width="3" />
            <line x1="0" y1="0" x2="0" y2="-34" stroke="#FFFBEB" stroke-width="3" />
            <polygon points="0,-34 26,-25 0,-16" fill="#E76F51" class=" waving-flag" />
            <text
              x="0"
              y="-44"
              text-anchor="middle"
              fill="#1F2937"
              font-size="12"
              font-weight="700"
              class="summit-label"
            >
              LA CUMBRE
            </text>
          </g>

          <!-- 11. Los 6 Campamentos (Check-points Interactivos) -->
          <g
            v-for="camp in enrichedCamps"
            :key="camp.order"
            class="camp-checkpoint"
            :class="{
              completed: camp.status === 'completed',
              'in-progress': camp.status === 'in_progress',
              selected: selectedCamp?.order === camp.order,
            }"
            :transform="`translate(${camp.x}, ${camp.y})`"
            role="button"
            tabindex="0"
            :aria-label="`Campamento ${camp.order}: ${camp.title}`"
            @click="selectCamp(camp)"
            @keydown.enter="selectCamp(camp)"
          >
            <!-- Plataforma de roca del campamento -->
            <ellipse cx="0" cy="10" rx="44" ry="12" fill="#8D5B3C" />
            <ellipse cx="0" cy="6" rx="44" ry="10" fill="#F4C078" />

            <!-- Bandera ondeando en Coral (#E76F51) al completar o Ocre/Aguamarina -->
            <line x1="18" y1="4" x2="18" y2="-36" stroke="#1F2937" stroke-width="2.5" />
            <path
              d="M 18 -36 L 44 -28 L 18 -20 Z"
              :fill="
                camp.status === 'completed'
                  ? '#E76F51'
                  : camp.status === 'in_progress'
                    ? '#2A9D8F'
                    : '#9CA3AF'
              "
              class="camp-flag"
            />

            <!-- Nodo circular con número del Hito -->
            <circle
              cx="0"
              cy="0"
              r="18"
              :fill="
                camp.status === 'completed'
                  ? '#10B981'
                  : camp.status === 'in_progress'
                    ? '#2A9D8F'
                    : '#FFFFFF'
              "
              :stroke="selectedCamp?.order === camp.order ? '#C2822B' : '#1F2937'"
              stroke-width="3"
            />
            <text
              x="0"
              y="5"
              text-anchor="middle"
              :fill="camp.status === 'pending' ? '#1F2937' : '#FFFFFF'"
              font-size="13"
              font-weight="700"
            >
              {{ camp.order }}
            </text>

            <!-- Etiqueta flotante lateral del Campamento -->
            <g :transform="camp.labelSide === 'left' ? 'translate(-225, -18)' : 'translate(54, -18)'">
              <rect
                x="0"
                y="0"
                width="172"
                height="40"
                rx="8"
                fill="#FFFFFF"
                fill-opacity="0.94"
                :stroke="selectedCamp?.order === camp.order ? '#C2822B' : '#E5E7EB'"
                stroke-width="2"
              />
              <text x="10" y="16" fill="#C2822B" font-size="10" font-weight="700">
                HITO {{ camp.order }} · {{ camp.percentage }}%
              </text>
              <text x="10" y="31" fill="#1F2937" font-size="11" font-weight="600">
                {{ camp.title.length > 23 ? camp.title.slice(0, 23) + '...' : camp.title }}
              </text>
            </g>
          </g>

          <!-- 12. Nubes de Primer Plano en la Base de la Montaña -->
          <g class="foreground-clouds">
            <path
              d="M 0 1020 L 0 905 Q 65 865 135 900 Q 210 855 290 915 Q 375 885 450 935 Q 540 885 630 920 Q 720 860 810 905 Q 860 885 900 915 L 900 1020 Z"
              fill="#5A527A"
              opacity="0.82"
            />
            <path
              d="M 0 1020 L 0 945 Q 95 905 185 948 Q 290 915 390 960 Q 510 918 615 955 Q 735 905 830 948 L 900 940 L 900 1020 Z"
              fill="#3A385B"
              opacity="0.92"
            />
          </g>

          <!-- 13. Avatar del Guerrero / Explorador Articulado e Interactivo -->
          <g
            id="warrior-avatar"
            ref="warriorGroupRef"
            class="warrior-character"
            :class="{ walking: isWalking }"
            transform="translate(330, 880)"
          >
            <g :transform="warriorFacingLeft ? 'scale(-1, 1)' : 'scale(1, 1)'">
              <!-- Halo de ubicación del personaje -->
              <ellipse cx="0" cy="2" rx="16" ry="6" fill="rgba(194, 130, 43, 0.45)" />

              <!-- Pierna trasera articulada -->
              <line
                class="limb leg-back"
                x1="-2"
                y1="-18"
                x2="-9"
                y2="0"
                stroke="#4A1D1F"
                stroke-width="4.5"
                stroke-linecap="round"
              />
              <!-- Pierna delantera articulada -->
              <line
                class="limb leg-front"
                x1="2"
                y1="-18"
                x2="9"
                y2="0"
                stroke="#6B272A"
                stroke-width="4.5"
                stroke-linecap="round"
              />

              <!-- Mochila de expedición Ocre Tierra (#C2822B) -->
              <rect
                x="-14"
                y="-38"
                width="11"
                height="18"
                rx="4"
                fill="#C2822B"
                stroke="#1F2937"
                stroke-width="1.5"
              />

              <!-- Torso (Chaqueta Coral / Roja de alpinista como en la ilustración) -->
              <path
                d="M -5 -39 L 7 -39 L 9 -18 L -6 -18 Z"
                fill="#E76F51"
                stroke="#1F2937"
                stroke-width="1.5"
              />

              <!-- Brazo delantero saludando / impulsando el ascenso -->
              <path
                class="limb arm-front"
                d="M 5 -35 Q 14 -38 17 -46"
                fill="none"
                stroke="#E76F51"
                stroke-width="4"
                stroke-linecap="round"
              />

              <!-- Cabeza y cabello al viento -->
              <circle
                cx="2"
                cy="-47"
                r="7.5"
                fill="#F4A261"
                stroke="#1F2937"
                stroke-width="1.5"
              />
              <path
                d="M -6 -49 Q -2 -58 9 -53 Q 6 -47 -4 -47 Z"
                fill="#2B1B17"
              />
            </g>
          </g>
        </svg>
      </div>

      <!-- Panel Lateral Interactivo del Campamento Seleccionado -->
      <aside class="camp-inspector">
        <div v-if="selectedCamp" class="card inspector-card">
          <div class="inspector-top">
            <span class="badge badge-primary">Campamento {{ selectedCamp.order }} de 6</span>
            <span
              class="badge"
              :class="
                selectedCamp.status === 'completed'
                  ? 'badge-success'
                  : selectedCamp.status === 'in_progress'
                    ? 'badge-secondary'
                    : 'badge-neutral'
              "
            >
              {{
                selectedCamp.status === 'completed'
                  ? 'Superado'
                  : selectedCamp.status === 'in_progress'
                    ? 'En Ascenso'
                    : 'Por Explorar'
              }}
            </span>
          </div>

          <h2>{{ selectedCamp.title }}</h2>
          <p class="inspector-subtitle">{{ selectedCamp.subtitle }}</p>

          <div class="progress-bar-wrap">
            <div class="progress-bar-labels">
              <span>Progreso del Campamento</span>
              <strong>{{ selectedCamp.percentage }}%</strong>
            </div>
            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{ width: `${selectedCamp.percentage}%` }"
              />
            </div>
            <span class="lessons-counter">
              {{ selectedCamp.completed_lessons }} de {{ selectedCamp.total_lessons }} lecciones completadas
            </span>
          </div>

          <button
            type="button"
            class="btn btn-primary full-width-btn"
            @click="goToModule(selectedCamp.module_id)"
          >
            Continuar ascenso en este módulo
          </button>
        </div>

        <div class="card quick-camps-card">
          <h3>Selector Rápido de Estaciones</h3>
          <p class="helper-text">
            Pulsa cualquier estación para desplazar al guerrero por el sendero de la montaña:
          </p>
          <div class="quick-camps-list">
            <button
              v-for="camp in enrichedCamps"
              :key="camp.order"
              type="button"
              class="quick-camp-btn"
              :class="{ active: selectedCamp?.order === camp.order }"
              @click="selectCamp(camp)"
            >
              <span class="quick-step">Hito {{ camp.order }}</span>
              <span class="quick-title">{{ camp.title }}</span>
              <span class="quick-pct">{{ camp.percentage }}%</span>
            </button>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.expedition-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
}

.expedition-header h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  max-width: 680px;
  margin-top: var(--space-2);
  margin-bottom: 0;
}

.summary-pill {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
}

.summary-stat {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.76rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 1.25rem;
  color: var(--color-primary);
}

.summary-divider {
  width: 1px;
  height: 34px;
  background-color: var(--border-subtle);
}

.expedition-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.95fr);
  gap: var(--space-6);
  align-items: start;
}

.mountain-canvas-card {
  padding: var(--space-3);
  overflow: hidden;
}

.mountain-svg {
  width: 100%;
  height: auto;
  display: block;
  border-radius: var(--radius-sm);
}

.camp-checkpoint {
  cursor: pointer;
  transition: filter var(--transition-fast);
}

.camp-checkpoint:hover {
  filter: brightness(1.08);
}

/* Animaciones ambientales suaves y del personaje */
@keyframes sunPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.92;
  }
  50% {
    transform: scale(1.06);
    opacity: 1;
  }
}

.sun-pulse {
  transform-origin: 495px 115px;
  animation: sunPulse 4s ease-in-out infinite;
}

@keyframes birdFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-6px);
  }
}

.bird-1 {
  animation: birdFloat 3.4s ease-in-out infinite;
}
.bird-2 {
  animation: birdFloat 4.1s ease-in-out infinite 0.6s;
}
.bird-3 {
  animation: birdFloat 3.8s ease-in-out infinite 1.1s;
}

/* Movimiento de extremidades del personaje al caminar o respirar */
@keyframes warriorIdle {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2.5px);
  }
}

@keyframes legSwingFront {
  0%, 100% {
    transform: rotate(-18deg);
  }
  50% {
    transform: rotate(18deg);
  }
}

@keyframes legSwingBack {
  0%, 100% {
    transform: rotate(18deg);
  }
  50% {
    transform: rotate(-18deg);
  }
}

.warrior-character .limb {
  transform-box: fill-box;
  transform-origin: top center;
}

.warrior-character.walking .leg-front {
  animation: legSwingFront 0.32s linear infinite;
}

.warrior-character.walking .leg-back {
  animation: legSwingBack 0.32s linear infinite;
}

.camp-inspector {
  display: grid;
  gap: var(--space-5);
}

.inspector-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.inspector-subtitle {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: var(--space-1);
}

.progress-bar-wrap {
  margin: var(--space-5) 0;
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  background-color: var(--bg-app);
  border: 1px solid var(--border-subtle);
}

.progress-bar-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.84rem;
  margin-bottom: var(--space-2);
}

.progress-track {
  width: 100%;
  height: 10px;
  border-radius: var(--radius-pill);
  background-color: var(--border-subtle);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-secondary) 0%, var(--color-primary) 100%);
  transition: width var(--transition-normal);
}

.lessons-counter {
  display: block;
  margin-top: var(--space-2);
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.full-width-btn {
  width: 100%;
}

.helper-text {
  font-size: 0.84rem;
  color: var(--text-secondary);
  margin: var(--space-1) 0 var(--space-3);
}

.quick-camps-list {
  display: grid;
  gap: var(--space-2);
}

.quick-camp-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
  font-family: var(--font-family-base);
  cursor: pointer;
  text-align: left;
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.quick-camp-btn:hover {
  border-color: var(--color-secondary);
}

.quick-camp-btn.active {
  border-color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

.quick-step {
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--color-primary-hover);
  white-space: nowrap;
}

.quick-title {
  flex: 1;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.quick-pct {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--color-secondary);
}

@media (max-width: 1024px) {
  .expedition-layout {
    grid-template-columns: 1fr;
  }
}
</style>
