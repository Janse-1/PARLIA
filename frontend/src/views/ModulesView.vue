<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { learningService } from '../services/learningService'
import { useProgressStore } from '../stores/progress'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const progressStore = useProgressStore()
const authStore = useAuthStore()

const modules = ref([])
const loading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    const modsPromise = learningService.getModules()
    const progPromise = authStore.isAuthenticated
      ? progressStore.fetchMyProgress().catch(() => null)
      : Promise.resolve(null)
    const [modsData] = await Promise.all([modsPromise, progPromise])
    modules.value = modsData
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'No se pudieron cargar los módulos.'
  } finally {
    loading.value = false
  }
})

const enrichedModules = computed(() => {
  const q = (route.query.q || '').toString().trim().toLowerCase()
  return modules.value
    .map((m) => {
      const summary = progressStore.getModuleSummary(m.id)
      return {
        ...m,
        status: summary.status,
        percentage: summary.percentage,
        completed_lessons: summary.completed_lessons,
      }
    })
    .filter((m) => {
      if (!q) return true
      return (
        m.title.toLowerCase().includes(q) ||
        m.description.toLowerCase().includes(q)
      )
    })
})

function statusLabel(status) {
  if (status === 'completed') return 'Completado'
  if (status === 'in_progress') return 'En Progreso'
  return 'Pendiente'
}

function statusBadgeClass(status) {
  if (status === 'completed') return 'badge-success'
  if (status === 'in_progress') return 'badge-secondary'
  return 'badge-neutral'
}
</script>

<template>
  <section class="modules-view">
    <header class="view-header">
      <div>
        <span class="badge badge-primary">Ruta Formativa Oficial</span>
        <h1>Módulos del Laboratorio PARLIA</h1>
        <p class="subtitle">
          Recorre los 6 ejes pedagógicos diseñados para desarrollar criterio técnico y reflexivo frente a la Inteligencia Artificial Generativa.
        </p>
      </div>

      <router-link to="/progress" class="btn btn-secondary">
        Ver Mapa de Ascenso ({{ progressStore.overallPercentage }}%)
      </router-link>
    </header>

    <p v-if="errorMessage" class="callout callout-warning">{{ errorMessage }}</p>

    <div v-if="loading" class="card">
      <p>Cargando catálogo de módulos...</p>
    </div>

    <div v-else class="modules-grid">
      <article
        v-for="mod in enrichedModules"
        :key="mod.id"
        class="card module-card"
      >
        <div>
          <div class="module-card-top">
            <span class="module-number">Módulo {{ mod.order }}</span>
            <span class="badge" :class="statusBadgeClass(mod.status)">
              {{ statusLabel(mod.status) }}
            </span>
          </div>

          <h2>{{ mod.title }}</h2>
          <p class="module-desc">{{ mod.description }}</p>
        </div>

        <div class="module-card-footer">
          <span class="meta-text">
            {{ mod.completed_lessons || 0 }} / {{ mod.lessons_count }} lecciones completadas
          </span>
          <router-link :to="`/modules/${mod.id}`" class="btn btn-primary btn-sm">
            Explorar Módulo
          </router-link>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
}

.view-header h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  max-width: 720px;
  margin-top: var(--space-2);
  margin-bottom: 0;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
}

.module-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.module-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.module-number {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-primary);
}

.module-desc {
  color: var(--text-secondary);
  font-size: 0.92rem;
  margin: var(--space-3) 0 var(--space-5);
}

.module-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-subtle);
}

.meta-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.btn-sm {
  padding: 8px 14px;
  font-size: 0.84rem;
}
</style>
