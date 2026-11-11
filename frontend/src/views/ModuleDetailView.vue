<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { learningService } from '../services/learningService'
import { useProgressStore } from '../stores/progress'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const progressStore = useProgressStore()
const authStore = useAuthStore()

const moduleData = ref(null)
const loading = ref(true)
const errorMessage = ref('')

async function loadModule(moduleId) {
  loading.value = true
  errorMessage.value = ''
  try {
    const modPromise = learningService.getModuleDetail(moduleId)
    const progPromise = authStore.isAuthenticated
      ? progressStore.fetchMyProgress().catch(() => null)
      : Promise.resolve(null)
    const [mod] = await Promise.all([modPromise, progPromise])
    moduleData.value = mod
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'No se pudo cargar el detalle del módulo.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadModule(route.params.id)
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId) loadModule(newId)
  }
)

function statusLabel(lessonId) {
  const st = progressStore.getLessonStatus(lessonId)
  if (st === 'completed') return 'Completada'
  if (st === 'in_progress') return 'En Progreso'
  return 'Pendiente'
}

function statusBadgeClass(lessonId) {
  const st = progressStore.getLessonStatus(lessonId)
  if (st === 'completed') return 'badge-success'
  if (st === 'in_progress') return 'badge-secondary'
  return 'badge-neutral'
}
</script>

<template>
  <section class="module-detail-view">
    <nav class="breadcrumb" aria-label="Ruta de navegación">
      <router-link to="/modules">Módulos</router-link>
      <span>/</span>
      <span v-if="moduleData">Módulo {{ moduleData.order }}</span>
    </nav>

    <p v-if="errorMessage" class="callout callout-warning">{{ errorMessage }}</p>

    <div v-if="loading" class="card">
      <p>Cargando lecciones del módulo...</p>
    </div>

    <template v-else-if="moduleData">
      <header class="card module-banner">
        <span class="badge badge-primary">Módulo {{ moduleData.order }} de 6</span>
        <h1>{{ moduleData.title }}</h1>
        <p class="subtitle">{{ moduleData.description }}</p>
      </header>

      <div class="lessons-section">
        <h2>Lecciones del Módulo</h2>

        <div class="lessons-list">
          <article
            v-for="lesson in moduleData.lessons"
            :key="lesson.id"
            class="card lesson-item"
          >
            <div class="lesson-info">
              <span class="lesson-index">{{ moduleData.order }}.{{ lesson.order }}</span>
              <div>
                <h3>{{ lesson.title }}</h3>
                <span class="lesson-meta">
                  Lectura y práctica estimada: {{ lesson.estimated_minutes }} min
                </span>
              </div>
            </div>

            <div class="lesson-right">
              <span class="badge" :class="statusBadgeClass(lesson.id)">
                {{ statusLabel(lesson.id) }}
              </span>
              <router-link :to="`/lessons/${lesson.id}`" class="btn btn-primary">
                Abrir Lección
              </router-link>
            </div>
          </article>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-4);
}

.module-banner {
  margin-bottom: var(--space-6);
}

.module-banner h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
  margin-bottom: 0;
}

.lessons-section h2 {
  margin-bottom: var(--space-4);
}

.lessons-list {
  display: grid;
  gap: var(--space-4);
}

.lesson-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.lesson-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.lesson-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background-color: var(--color-secondary-soft);
  color: var(--color-secondary-hover);
  font-weight: 700;
}

.lesson-meta {
  font-size: 0.82rem;
  color: var(--text-secondary);
}
</style>
