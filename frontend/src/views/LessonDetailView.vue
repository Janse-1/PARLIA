<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { learningService } from '../services/learningService'
import { useProgressStore } from '../stores/progress'
import FormativeActivity from '../components/FormativeActivity.vue'

const route = useRoute()
const progressStore = useProgressStore()

const currentLesson = ref(null)
const loading = ref(true)
const savingProgress = ref(false)
const errorMessage = ref('')

const lessonStatus = computed(() => {
  if (!currentLesson.value) return 'pending'
  return progressStore.getLessonStatus(currentLesson.value.id)
})

const isCompleted = computed(() => lessonStatus.value === 'completed')

const contentParagraphs = computed(() => {
  return (currentLesson.value?.content || '')
    .split('\n\n')
    .map((p) => p.trim())
    .filter(Boolean)
})

async function loadLesson(lessonId) {
  loading.value = true
  errorMessage.value = ''
  try {
    const lesson = await learningService.getLessonDetail(lessonId)
    currentLesson.value = lesson

    // Al abrir la lección, registrar automáticamente estado in_progress
    // (el backend preserva completed si ya estaba completada)
    await progressStore.updateLessonProgress(lesson.id, 'in_progress')
  } catch (err) {
    errorMessage.value = err.response?.data?.message || 'No se pudo cargar la lección.'
  } finally {
    loading.value = false
  }
}

async function markCompleted() {
  if (!currentLesson.value || savingProgress.value) return
  savingProgress.value = true
  try {
    await progressStore.updateLessonProgress(currentLesson.value.id, 'completed')
  } finally {
    savingProgress.value = false
  }
}

onMounted(() => {
  loadLesson(route.params.id)
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId) loadLesson(newId)
  }
)
</script>

<template>
  <section class="lesson-detail-view">
    <nav v-if="currentLesson" class="breadcrumb" aria-label="Ruta de navegación">
      <router-link to="/modules">Módulos</router-link>
      <span>/</span>
      <router-link :to="`/modules/${currentLesson.module_id}`">
        Módulo {{ currentLesson.module_order }}
      </router-link>
      <span>/</span>
      <span>Lección {{ currentLesson.order }}</span>
    </nav>

    <p v-if="errorMessage" class="callout callout-warning">{{ errorMessage }}</p>

    <div v-if="loading" class="card">
      <p>Cargando contenido pedagógico de la lección...</p>
    </div>

    <article v-else-if="currentLesson" class="card lesson-reader">
      <header class="lesson-header">
        <div class="lesson-badges">
          <span class="badge badge-primary">Módulo {{ currentLesson.module_order }}</span>
          <span class="badge badge-neutral">Tiempo estimado: {{ currentLesson.estimated_minutes }} min</span>
          <span v-if="isCompleted" class="badge badge-success">Lección Completada</span>
          <span v-else class="badge badge-secondary">En Progreso</span>
        </div>
        <h1>{{ currentLesson.title }}</h1>
      </header>

      <div class="lesson-blocks">
        <p v-for="(paragraph, idx) in contentParagraphs" :key="idx" class="reading-block">
          {{ paragraph }}
        </p>
      </div>

      <div class="callout">
        <strong>Principio de Verificación Activa:</strong>
        Contrasta siempre las salidas del modelo con documentación técnica primaria, normas vigentes y pruebas reproducibles en tu entorno local.
      </div>

      <section v-if="currentLesson.media_assets?.length" class="media-section">
        <h2>Recursos Multimedia Externos</h2>
        <div class="media-list">
          <a
            v-for="asset in currentLesson.media_assets"
            :key="asset.id"
            :href="asset.url"
            target="_blank"
            rel="noopener noreferrer"
            class="media-card"
          >
            <div>
              <span class="badge badge-secondary">{{ asset.asset_type_display }}</span>
              <h3>{{ asset.title }}</h3>
              <p v-if="asset.description">{{ asset.description }}</p>
            </div>
            <span class="external-link-label">Abrir recurso</span>
          </a>
        </div>
      </section>

      <FormativeActivity
        v-if="currentLesson.activity_id"
        :activity-id="currentLesson.activity_id"
      />

      <footer class="lesson-actions">
        <button
          type="button"
          class="btn"
          :class="isCompleted ? 'btn-secondary' : 'btn-primary'"
          :disabled="savingProgress || isCompleted"
          @click="markCompleted"
        >
          {{
            savingProgress
              ? 'Guardando avance...'
              : isCompleted
                ? 'Lección completada y guardada'
                : 'Marcar lección como completada'
          }}
        </button>

        <div class="nav-buttons">
          <router-link
            v-if="currentLesson.previous_lesson_id"
            :to="`/lessons/${currentLesson.previous_lesson_id}`"
            class="btn btn-outline"
          >
            Lección Anterior
          </router-link>
          <router-link
            v-if="currentLesson.next_lesson_id"
            :to="`/lessons/${currentLesson.next_lesson_id}`"
            class="btn btn-outline"
          >
            Siguiente Lección
          </router-link>
          <router-link
            :to="`/modules/${currentLesson.module_id}`"
            class="btn btn-outline"
          >
            Volver al Módulo
          </router-link>
        </div>
      </footer>
    </article>
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

.lesson-reader {
  padding: var(--space-8);
}

.lesson-header {
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: var(--space-6);
}

.lesson-badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.lesson-blocks {
  display: grid;
  gap: var(--space-4);
}

.reading-block {
  font-size: 1rem;
  line-height: 1.75;
  color: var(--text-primary);
  margin: 0;
}

.media-section {
  margin-top: var(--space-6);
  padding-top: var(--space-5);
  border-top: 1px solid var(--border-subtle);
}

.media-section h2 {
  margin-bottom: var(--space-3);
}

.media-list {
  display: grid;
  gap: var(--space-3);
}

.media-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
  color: var(--text-primary);
}

.media-card h3 {
  margin-top: var(--space-2);
}

.media-card p {
  margin: var(--space-1) 0 0;
  font-size: 0.86rem;
  color: var(--text-secondary);
}

.external-link-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-secondary);
  white-space: nowrap;
}

.lesson-actions {
  margin-top: var(--space-8);
  padding-top: var(--space-5);
  border-top: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.nav-buttons {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

@media (max-width: 767px) {
  .lesson-reader {
    padding: var(--space-5);
  }
}
</style>
