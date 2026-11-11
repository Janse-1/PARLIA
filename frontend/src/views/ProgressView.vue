<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import anime from 'animejs/lib/anime.es.js'
import { useProgressStore } from '../stores/progress'

const router = useRouter()
const progressStore = useProgressStore()

const selectedOrder = ref(1)
const animatedOverall = ref(0)
const animatedCompleted = ref(0)
const animatedHours = ref('0.0')
const animatedModulesDone = ref(0)
const barRefs = ref([])
const radialRefs = ref([])

const defaultMilestones = [
  {
    order: 1,
    code: 'MÓDULO 01',
    defaultTitle: 'Fundamentos de la Inteligencia Artificial Generativa',
    domain: 'Arquitectura LLM y Predicción de Tokens',
    estimatedMinutesPerLesson: 25,
    focusSkill: 'Criterio Algorítmico',
  },
  {
    order: 2,
    code: 'MÓDULO 02',
    defaultTitle: 'Ingeniería de Prompts',
    domain: 'Formulación Estructurada, Rol y Restricciones',
    estimatedMinutesPerLesson: 30,
    focusSkill: 'Prompting Técnico',
  },
  {
    order: 3,
    code: 'MÓDULO 03',
    defaultTitle: 'Verificaciones',
    domain: 'Auditoría de Salidas y Detección de Alucinaciones',
    estimatedMinutesPerLesson: 35,
    focusSkill: 'Auditoría y Pruebas',
  },
  {
    order: 4,
    code: 'MÓDULO 04',
    defaultTitle: 'Ética, Privacidad e Integridad Académica',
    domain: 'Trazabilidad, Datos Sensibles y Declaración de Uso',
    estimatedMinutesPerLesson: 25,
    focusSkill: 'Ética e Integridad',
  },
  {
    order: 5,
    code: 'MÓDULO 05',
    defaultTitle: 'Aplicación en investigación, redacción',
    domain: 'Síntesis Científica y Voz Analítica Propia',
    estimatedMinutesPerLesson: 30,
    focusSkill: 'Síntesis e Investigación',
  },
  {
    order: 6,
    code: 'MÓDULO 06',
    defaultTitle: 'Actividades finales',
    domain: 'Integración de Ingeniería Verificada',
    estimatedMinutesPerLesson: 40,
    focusSkill: 'Integración Profesional',
  },
]

const milestones = computed(() => {
  const byOrder = {}
  for (const m of progressStore.modules) {
    byOrder[m.order] = m
  }

  // Determinamos cuál es el primer módulo no completado para marcarlo como activo
  let activeFound = false

  return defaultMilestones.map((item) => {
    const apiMod = byOrder[item.order]
    const rawPct = apiMod?.percentage || 0
    const completedLessons = apiMod?.completed_lessons || 0
    const totalLessons = apiMod?.total_lessons || 2

    let nodeState = 'locked'
    if (rawPct >= 100 || apiMod?.status === 'completed') {
      nodeState = 'completed'
    } else if (!activeFound || rawPct > 0 || apiMod?.status === 'in_progress') {
      nodeState = 'active'
      activeFound = true
    }

    const investedMinutes =
      completedLessons * item.estimatedMinutesPerLesson +
      (nodeState === 'active' && completedLessons === 0 ? 10 : 0)

    return {
      ...item,
      module_id: apiMod?.module_id || item.order,
      title: apiMod?.title || item.defaultTitle,
      percentage: rawPct,
      completed_lessons: completedLessons,
      total_lessons: totalLessons,
      nodeState,
      investedMinutes,
    }
  })
})

const completedModulesCount = computed(
  () => milestones.value.filter((m) => m.nodeState === 'completed').length
)

const totalInvestedHours = computed(() => {
  const totalMins = milestones.value.reduce((acc, m) => acc + m.investedMinutes, 0)
  return (totalMins / 60).toFixed(1)
})

const selectedMilestone = computed(
  () => milestones.value.find((m) => m.order === selectedOrder.value) || milestones.value[0]
)

// Habilidades técnicas calculadas a partir del avance modular real
const technicalSkills = computed(() => {
  const m = milestones.value
  const getPct = (ord) => m.find((x) => x.order === ord)?.percentage || 0

  const promptingScore = Math.round(getPct(1) * 0.35 + getPct(2) * 0.65)
  const auditScore = Math.round(getPct(3) * 0.7 + getPct(6) * 0.3)
  const ethicsScore = Math.round(getPct(4) * 0.75 + getPct(5) * 0.25)
  const codeResearchScore = Math.round((getPct(2) + getPct(3) + getPct(5) + getPct(6)) / 4)

  return [
    {
      key: 'prompting',
      label: 'Ingeniería de Prompts',
      desc: 'Estructuración de contexto, rol y restricciones',
      percentage: promptingScore,
      color: '#FF5B26',
    },
    {
      key: 'audit',
      label: 'Auditoría Algorítmica',
      desc: 'Contrastación de fuentes y detección de alucinaciones',
      percentage: auditScore,
      color: '#20A4B8',
    },
    {
      key: 'ethics',
      label: 'Ética e Integridad',
      desc: 'Privacidad de datos y trazabilidad académica',
      percentage: ethicsScore,
      color: '#F99D1C',
    },
    {
      key: 'code',
      label: 'Código e Investigación',
      desc: 'Validación de algoritmos y síntesis técnica',
      percentage: codeResearchScore,
      color: '#10B981',
    },
  ]
})

function selectMilestone(order) {
  selectedOrder.value = order
}

function goToModule(moduleId) {
  router.push(`/modules/${moduleId}`)
}

function getStateLabel(state) {
  if (state === 'completed') return 'Completado'
  if (state === 'active') return 'Activo'
  return 'Bloqueado'
}

function runDashboardAnimations() {
  const counterTarget = {
    overall: 0,
    completed: 0,
    hours: 0,
    mods: 0,
  }

  anime({
    targets: counterTarget,
    overall: progressStore.overallPercentage || 0,
    completed: progressStore.completedLessons || 0,
    hours: parseFloat(totalInvestedHours.value) || 0,
    mods: completedModulesCount.value || 0,
    duration: 1100,
    easing: 'easeOutExpo',
    update() {
      animatedOverall.value = Math.round(counterTarget.overall)
      animatedCompleted.value = Math.round(counterTarget.completed)
      animatedHours.value = counterTarget.hours.toFixed(1)
      animatedModulesDone.value = Math.round(counterTarget.mods)
    },
  })

  // Animación de barras de calibración por módulo
  barRefs.value.forEach((barEl) => {
    if (!barEl) return
    const targetPct = Number(barEl.dataset.pct || 0)
    anime({
      targets: barEl,
      width: ['0%', `${targetPct}%`],
      duration: 1050,
      delay: 120,
      easing: 'easeOutCubic',
    })
  })

  // Animación de indicadores radiales SVG de habilidades técnicas
  const circumference = 2 * Math.PI * 36 // r = 36 -> ~226.19
  radialRefs.value.forEach((circleEl) => {
    if (!circleEl) return
    const pct = Number(circleEl.dataset.pct || 0)
    const offset = circumference - (pct / 100) * circumference
    circleEl.style.strokeDasharray = `${circumference}`
    anime({
      targets: circleEl,
      strokeDashoffset: [circumference, offset],
      duration: 1200,
      delay: 180,
      easing: 'easeOutCubic',
    })
  })
}

function setBarRef(el) {
  if (el && !barRefs.value.includes(el)) {
    barRefs.value.push(el)
  }
}

function setRadialRef(el) {
  if (el && !radialRefs.value.includes(el)) {
    radialRefs.value.push(el)
  }
}

onMounted(async () => {
  try {
    await progressStore.fetchMyProgress()
  } catch {
    // Manejado por el store
  }
  const activeItem = milestones.value.find((m) => m.nodeState === 'active')
  if (activeItem) {
    selectedOrder.value = activeItem.order
  }
  await nextTick()
  runDashboardAnimations()
})

watch(
  () => progressStore.overallPercentage,
  async () => {
    await nextTick()
    runDashboardAnimations()
  }
)
</script>

<template>
  <section class="mastery-dashboard">
    <!-- ENCABEZADO EJECUTIVO -->
    <header class="dashboard-header">
      <div>
        <span class="badge badge-secondary">TELEMETRÍA DE APRENDIZAJE NO PUNITIVO</span>
        <h1>Dashboard de Hitos y Maestría Técnica</h1>
        <p class="header-subtitle">
          Monitorea tu calibración conceptual en los 6 ejes oficiales de ParLIA. Cada hito refleja comprensión verificada y práctica reflexiva.
        </p>
      </div>

      <button
        type="button"
        class="btn btn-primary"
        @click="goToModule(selectedMilestone.module_id)"
      >
        Continuar en {{ selectedMilestone.code }}
      </button>
    </header>

    <!-- TARJETAS KPI SUPERIORES CON CONTADORES ANIME.JS -->
    <div class="kpi-strip">
      <article class="card kpi-card">
        <span class="kpi-label">ÍNDICE DE MAESTRÍA GLOBAL</span>
        <div class="kpi-value-row">
          <strong class="kpi-number">{{ animatedOverall }}%</strong>
          <span class="kpi-tag">Calibrado</span>
        </div>
        <div class="kpi-micro-bar">
          <div class="kpi-micro-fill" :style="{ width: `${animatedOverall}%` }" />
        </div>
      </article>

      <article class="card kpi-card">
        <span class="kpi-label">LECCIONES VERIFICADAS</span>
        <div class="kpi-value-row">
          <strong class="kpi-number">
            {{ animatedCompleted }} <small>/ {{ progressStore.totalLessons }}</small>
          </strong>
          <span class="kpi-tag">Unidades</span>
        </div>
        <p class="kpi-foot">Progreso persistido en tiempo real</p>
      </article>

      <article class="card kpi-card">
        <span class="kpi-label">MÓDULOS CONSOLIDADOS</span>
        <div class="kpi-value-row">
          <strong class="kpi-number">{{ animatedModulesDone }} <small>/ 6</small></strong>
          <span class="kpi-tag">Ejes</span>
        </div>
        <p class="kpi-foot">Ruta oficial Facultad de Ingeniería</p>
      </article>

      <article class="card kpi-card">
        <span class="kpi-label">TIEMPO DE ESTUDIO ESTIMADO</span>
        <div class="kpi-value-row">
          <strong class="kpi-number">{{ animatedHours }} <small>h</small></strong>
          <span class="kpi-tag">Práctica</span>
        </div>
        <p class="kpi-foot">Dedicación formativa acumulada</p>
      </article>
    </div>

    <!-- STEPPER INTERACTIVO HORIZONTAL DE 6 NODOS -->
    <div class="card stepper-panel">
      <div class="panel-top-bar">
        <div>
          <span class="panel-code">RUTA DE CALIBRACIÓN MODULAR</span>
          <h2>Línea de Tiempo de los 6 Hitos de Ingeniería</h2>
        </div>
        <div class="stepper-legend">
          <span class="legend-item"><i class="dot completed" /> Completado</span>
          <span class="legend-item"><i class="dot active" /> Activo</span>
          <span class="legend-item"><i class="dot locked" /> Bloqueado</span>
        </div>
      </div>

      <div class="horizontal-stepper" role="tablist" aria-label="Hitos de progreso">
        <button
          v-for="item in milestones"
          :key="item.order"
          type="button"
          class="stepper-node"
          :class="[
            item.nodeState,
            { selected: selectedOrder === item.order },
          ]"
          @click="selectMilestone(item.order)"
        >
          <div class="node-header-line">
            <span class="node-indicator">
              <svg v-if="item.nodeState === 'completed'" viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="3" fill="none">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span v-else>{{ item.order }}</span>
            </span>
            <span class="node-code-text">{{ item.code }}</span>
            <span class="node-pct-badge">{{ item.percentage }}%</span>
          </div>

          <strong class="node-title-short">{{ item.title }}</strong>

          <div class="node-calibration-track">
            <div
              :ref="setBarRef"
              class="node-calibration-fill"
              :data-pct="item.percentage"
            />
          </div>

          <div class="node-meta-foot">
            <span>{{ item.completed_lessons }}/{{ item.total_lessons }} lecciones</span>
            <span>{{ item.investedMinutes }} min</span>
          </div>
        </button>
      </div>
    </div>

    <!-- GRILLA PRINCIPAL: TIMELINE DETALLADO (IZQUIERDA) + RADIALES DE HABILIDADES (DERECHA) -->
    <div class="dashboard-main-grid">
      <!-- Columna Izquierda: Desglose de Hitos y Acceso Rápido -->
      <div class="card milestones-list-card">
        <div class="panel-top-bar">
          <div>
            <span class="panel-code">DESGLOSE EJECUTIVO POR EJE</span>
            <h2>Estado Detallado de Módulos</h2>
          </div>
        </div>

        <div class="milestone-rows">
          <article
            v-for="item in milestones"
            :key="item.order"
            class="milestone-row"
            :class="[item.nodeState, { focused: selectedOrder === item.order }]"
            @click="selectMilestone(item.order)"
          >
            <div class="row-left">
              <div class="row-Order-box">0{{ item.order }}</div>
              <div class="row-info">
                <div class="row-title-line">
                  <h3>{{ item.title }}</h3>
                  <span class="state-chip" :class="item.nodeState">
                    {{ getStateLabel(item.nodeState) }}
                  </span>
                </div>
                <p class="row-domain">{{ item.domain }}</p>

                <div class="row-metrics-inline">
                  <span>Lecciones: <strong>{{ item.completed_lessons }}/{{ item.total_lessons }}</strong></span>
                  <span>Tiempo invertido: <strong>{{ item.investedMinutes }} min</strong></span>
                  <span>Competencia: <strong>{{ item.focusSkill }}</strong></span>
                </div>
              </div>
            </div>

            <div class="row-right">
              <div class="row-pct-block">
                <strong class="row-pct-num">{{ item.percentage }}%</strong>
                <div class="row-bar">
                  <div class="row-bar-fill" :style="{ width: `${item.percentage}%` }" />
                </div>
              </div>

              <button
                type="button"
                class="btn btn-outline btn-access"
                @click.stop="goToModule(item.module_id)"
              >
                {{ item.percentage > 0 ? 'Continuar' : 'Abrir Módulo' }} →
              </button>
            </div>
          </article>
        </div>
      </div>

      <!-- Columna Derecha: Matriz de Habilidades Técnicas con Indicadores Radiales -->
      <aside class="skills-sidebar">
        <div class="card skills-card">
          <span class="panel-code">MATRIZ DE COMPETENCIAS</span>
          <h2>Habilidades Técnicas Calibradas</h2>
          <p class="skills-desc">
            Indicadores radiales calculados en función de tu avance en formulación de prompts, verificación algorítmica, ética e investigación.
          </p>

          <div class="radial-skills-grid">
            <div
              v-for="skill in technicalSkills"
              :key="skill.key"
              class="radial-skill-item"
            >
              <div class="radial-svg-wrap">
                <svg viewBox="0 0 88 88" width="84" height="84">
                  <circle
                    cx="44"
                    cy="44"
                    r="36"
                    fill="none"
                    stroke="var(--border-subtle)"
                    stroke-width="6"
                  />
                  <circle
                    :ref="setRadialRef"
                    cx="44"
                    cy="44"
                    r="36"
                    fill="none"
                    :stroke="skill.color"
                    stroke-width="6"
                    stroke-linecap="round"
                    :data-pct="skill.percentage"
                    transform="rotate(-90 44 44)"
                  />
                </svg>
                <strong class="radial-pct-text">{{ skill.percentage }}%</strong>
              </div>

              <div class="radial-skill-meta">
                <h3>{{ skill.label }}</h3>
                <p>{{ skill.desc }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tarjeta de Inspección del Hito Seleccionado -->
        <div v-if="selectedMilestone" class="card inspector-card">
          <span class="panel-code">INSPECTOR DE HITO · {{ selectedMilestone.code }}</span>
          <h3>{{ selectedMilestone.title }}</h3>
          <p class="inspector-domain">{{ selectedMilestone.domain }}</p>

          <div class="inspector-stats-grid">
            <div>
              <span>Estado Actual</span>
              <strong>{{ getStateLabel(selectedMilestone.nodeState) }}</strong>
            </div>
            <div>
              <span>Avance Real</span>
              <strong>{{ selectedMilestone.percentage }}%</strong>
            </div>
            <div>
              <span>Lecciones</span>
              <strong>{{ selectedMilestone.completed_lessons }} de {{ selectedMilestone.total_lessons }}</strong>
            </div>
            <div>
              <span>Tiempo Invertido</span>
              <strong>{{ selectedMilestone.investedMinutes }} min</strong>
            </div>
          </div>

          <button
            type="button"
            class="btn btn-primary full-width-btn"
            @click="goToModule(selectedMilestone.module_id)"
          >
            Ir a las Lecciones del {{ selectedMilestone.code }}
          </button>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.mastery-dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.dashboard-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.dashboard-header h1 {
  margin-top: var(--space-2);
}

.header-subtitle {
  margin: var(--space-1) 0 0;
  color: var(--text-secondary);
  max-width: 680px;
  font-size: 0.94rem;
}

/* KPI STRIP */
.kpi-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.kpi-card {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-2);
}

.kpi-label {
  font-family: var(--font-family-mono);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.kpi-value-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-2);
}

.kpi-number {
  font-family: var(--font-family-mono);
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.1;
}

.kpi-number small {
  font-size: 0.95rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.kpi-tag {
  font-size: 0.74rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: var(--color-secondary-soft);
  color: var(--color-secondary);
}

.kpi-micro-bar {
  height: 6px;
  background-color: var(--bg-subtle);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 4px;
}

.kpi-micro-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  transition: width 0.3s ease;
}

.kpi-foot {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-secondary);
}

/* STEPPER PANEL */
.stepper-panel {
  padding: var(--space-6);
}

.panel-top-bar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin-bottom: var(--space-5);
}

.panel-code {
  display: block;
  font-family: var(--font-family-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--color-secondary);
  letter-spacing: 0.06em;
  margin-bottom: 4px;
}

.stepper-legend {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
}

.dot.completed {
  background-color: var(--color-success);
}

.dot.active {
  background-color: var(--color-primary);
}

.dot.locked {
  background-color: var(--path-pending);
}

.horizontal-stepper {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--space-3);
}

.stepper-node {
  text-align: left;
  padding: var(--space-4);
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-3);
  transition: border-color var(--transition-fast), transform var(--transition-fast), background-color var(--transition-fast);
}

.stepper-node:hover {
  border-color: var(--color-secondary);
  transform: translateY(-2px);
}

.stepper-node.selected {
  border-color: var(--color-primary);
  background-color: var(--bg-surface);
}

.stepper-node.completed {
  border-top: 3px solid var(--color-success);
}

.stepper-node.active {
  border-top: 3px solid var(--color-primary);
}

.stepper-node.locked {
  border-top: 3px solid var(--path-pending);
  opacity: 0.82;
}

.node-header-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}

.node-indicator {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-family-mono);
  font-size: 0.76rem;
  font-weight: 700;
  background-color: var(--bg-subtle);
  color: var(--text-primary);
}

.stepper-node.completed .node-indicator {
  background-color: var(--color-success-soft);
  color: var(--color-success);
}

.stepper-node.active .node-indicator {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
}

.node-code-text {
  font-family: var(--font-family-mono);
  font-size: 0.68rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.node-pct-badge {
  font-family: var(--font-family-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-primary);
}

.node-title-short {
  font-size: 0.84rem;
  line-height: 1.35;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.3rem;
}

.node-calibration-track {
  height: 5px;
  background-color: var(--border-subtle);
  border-radius: 2px;
  overflow: hidden;
}

.node-calibration-fill {
  height: 100%;
  width: 0%;
  background-color: var(--color-secondary);
}

.stepper-node.completed .node-calibration-fill {
  background-color: var(--color-success);
}

.stepper-node.active .node-calibration-fill {
  background-color: var(--color-primary);
}

.node-meta-foot {
  display: flex;
  justify-content: space-between;
  font-size: 0.72rem;
  color: var(--text-secondary);
}

/* GRILLA PRINCIPAL DE 2 COLUMNAS */
.dashboard-main-grid {
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  gap: var(--space-5);
  align-items: start;
}

.milestones-list-card {
  padding: var(--space-6);
}

.milestone-rows {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.milestone-row {
  padding: var(--space-4);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--path-pending);
  border-radius: 4px;
  background-color: var(--bg-app);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  cursor: pointer;
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.milestone-row.completed {
  border-left-color: var(--color-success);
}

.milestone-row.active {
  border-left-color: var(--color-primary);
}

.milestone-row.focused {
  background-color: var(--bg-surface);
  border-color: var(--color-secondary);
}

.row-left {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  flex: 1;
}

.row-Order-box {
  font-family: var(--font-family-mono);
  font-size: 0.85rem;
  font-weight: 800;
  padding: 6px 9px;
  border-radius: 4px;
  background-color: var(--bg-subtle);
  color: var(--text-primary);
}

.row-info {
  flex: 1;
}

.row-title-line {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.row-title-line h3 {
  font-size: 0.98rem;
  margin: 0;
}

.state-chip {
  font-family: var(--font-family-mono);
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  text-transform: uppercase;
}

.state-chip.completed {
  background-color: var(--color-success-soft);
  color: var(--color-success);
}

.state-chip.active {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
}

.state-chip.locked {
  background-color: var(--bg-subtle);
  color: var(--text-secondary);
}

.row-domain {
  margin: 4px 0 8px;
  font-size: 0.84rem;
  color: var(--text-secondary);
}

.row-metrics-inline {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  font-size: 0.78rem;
  color: var(--text-secondary);
}

.row-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.row-pct-block {
  min-width: 88px;
  text-align: right;
}

.row-pct-num {
  font-family: var(--font-family-mono);
  font-size: 1rem;
  color: var(--text-primary);
  display: block;
  margin-bottom: 4px;
}

.row-bar {
  height: 5px;
  background-color: var(--border-subtle);
  border-radius: 2px;
  overflow: hidden;
}

.row-bar-fill {
  height: 100%;
  background-color: var(--color-secondary);
}

.btn-access {
  padding: 8px 12px;
  font-size: 0.82rem;
  white-space: nowrap;
}

/* SKILLS SIDEBAR */
.skills-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.skills-card,
.inspector-card {
  padding: var(--space-6);
}

.skills-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: var(--space-1);
  margin-bottom: var(--space-4);
}

.radial-skills-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.radial-skill-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  background-color: var(--bg-app);
}

.radial-svg-wrap {
  position: relative;
  width: 84px;
  height: 84px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.radial-pct-text {
  position: absolute;
  font-family: var(--font-family-mono);
  font-size: 0.88rem;
  font-weight: 800;
  color: var(--text-primary);
}

.radial-skill-meta h3 {
  font-size: 0.94rem;
  margin-bottom: 3px;
}

.radial-skill-meta p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.45;
}

.inspector-domain {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 4px;
}

.inspector-stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
  margin: var(--space-4) 0;
  padding: var(--space-3);
  border-radius: 4px;
  background-color: var(--bg-app);
  border: 1px solid var(--border-subtle);
}

.inspector-stats-grid span {
  display: block;
  font-size: 0.74rem;
  color: var(--text-secondary);
}

.inspector-stats-grid strong {
  font-size: 0.92rem;
  color: var(--text-primary);
}

.full-width-btn {
  width: 100%;
}

@media (max-width: 1120px) {
  .horizontal-stepper {
    grid-template-columns: repeat(3, 1fr);
  }

  .dashboard-main-grid {
    grid-template-columns: 1fr;
  }

  .kpi-strip {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .horizontal-stepper,
  .kpi-strip {
    grid-template-columns: 1fr;
  }

  .milestone-row {
    flex-direction: column;
    align-items: stretch;
  }

  .row-right {
    justify-content: space-between;
    border-top: 1px solid var(--border-subtle);
    padding-top: var(--space-3);
  }
}
</style>
