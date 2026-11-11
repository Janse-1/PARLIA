<script setup>
import { ref, onMounted, watch } from 'vue'
import { activityService } from '../services/activityService'

const props = defineProps({
  activityId: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['activity-completed'])

const activity = ref(null)
const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')

const selectedOption = ref(null)
const reflectionText = ref('')
const feedback = ref(null)

async function loadActivity(id) {
  if (!id) return
  loading.value = true
  errorMessage.value = ''
  selectedOption.value = null
  reflectionText.value = ''
  feedback.value = null

  try {
    activity.value = await activityService.getActivity(id)
  } catch (err) {
    errorMessage.value =
      err.response?.data?.message || 'No se pudo cargar la actividad formativa.'
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!activity.value || submitting.value) return
  errorMessage.value = ''

  const firstQuestion = activity.value.questions?.[0]
  const payload = {
    question_id: firstQuestion?.id || null,
    selected_option: selectedOption.value,
    reflection_text: reflectionText.value.trim() || null,
  }

  submitting.value = true
  try {
    const res = await activityService.submitAttempt(activity.value.id, payload)
    feedback.value = res.feedback
    emit('activity-completed', res)
  } catch (err) {
    errorMessage.value =
      err.response?.data?.message ||
      'Por favor selecciona una opción o escribe tu reflexión antes de enviar.'
  } finally {
    submitting.value = false
  }
}

function resetAttempt() {
  feedback.value = null
}

onMounted(() => {
  loadActivity(props.activityId)
})

watch(
  () => props.activityId,
  (newId) => {
    if (newId) loadActivity(newId)
  }
)
</script>

<template>
  <section class="formative-activity">
    <div v-if="loading" class="activity-box">
      <p>Cargando ejercicio formativo...</p>
    </div>

    <div v-else-if="activity" class="activity-box">
      <header class="activity-header">
        <span class="badge badge-primary">{{ activity.activity_type_display }}</span>
        <span class="badge badge-neutral">Sin calificación punitiva</span>
        <h2>{{ activity.title }}</h2>
        <p class="activity-desc">{{ activity.description }}</p>
      </header>

      <div v-for="question in activity.questions" :key="question.id" class="question-block">
        <p class="question-prompt">{{ question.prompt_text }}</p>

        <!-- Opciones de Selección Múltiple / Auditoría de Prompt -->
        <div
          v-if="question.options && question.options.length > 0"
          class="options-list"
          role="radiogroup"
          :aria-label="question.prompt_text"
        >
          <label
            v-for="opt in question.options"
            :key="opt.id"
            class="option-card"
            :class="{ selected: selectedOption === opt.id }"
          >
            <input
              v-model="selectedOption"
              type="radio"
              :name="`question-${question.id}`"
              :value="opt.id"
            />
            <span class="option-text">{{ opt.text }}</span>
          </label>
        </div>

        <!-- Campo de Reflexión Abierta -->
        <div v-else class="reflection-field">
          <label :for="`reflection-${question.id}`" class="reflection-label">
            Escribe tu análisis o reflexión técnica:
          </label>
          <textarea
            :id="`reflection-${question.id}`"
            v-model="reflectionText"
            rows="4"
            class="reflection-textarea"
            placeholder="Desarrolla aquí tu criterio técnico sin temor a equivocarse..."
          />
        </div>
      </div>

      <p v-if="errorMessage" class="callout callout-warning">{{ errorMessage }}</p>

      <!-- Retroalimentación Pedagógica Inmediata -->
      <div
        v-if="feedback"
        class="feedback-panel"
        :class="feedback.is_correct === false ? 'feedback-explore' : 'feedback-positive'"
      >
        <h3>{{ feedback.title }}</h3>
        <p>{{ feedback.explanation }}</p>
        <button type="button" class="btn btn-outline btn-sm" @click="resetAttempt">
          Probar otra respuesta
        </button>
      </div>

      <div class="activity-submit-bar">
        <button
          type="button"
          class="btn btn-secondary"
          :disabled="submitting"
          @click="handleSubmit"
        >
          {{ submitting ? 'Verificando análisis...' : 'Verificar y recibir retroalimentación' }}
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.formative-activity {
  margin-top: var(--space-8);
  padding-top: var(--space-6);
  border-top: 2px dashed var(--border-subtle);
}

.activity-box {
  padding: var(--space-6);
  border-radius: var(--radius-md);
  background-color: var(--bg-app);
  border: 1px solid var(--border-subtle);
}

.activity-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.activity-header h2 {
  width: 100%;
  margin-top: var(--space-2);
}

.activity-desc {
  width: 100%;
  color: var(--text-secondary);
  margin: 0;
  font-size: 0.92rem;
}

.question-block {
  margin-top: var(--space-4);
}

.question-prompt {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.options-list {
  display: grid;
  gap: var(--space-3);
}

.option-card {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  cursor: pointer;
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.option-card:hover {
  border-color: var(--color-secondary);
}

.option-card.selected {
  border-color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

.option-card input {
  margin-top: 4px;
  accent-color: var(--color-primary);
}

.option-text {
  font-size: 0.94rem;
  line-height: 1.5;
}

.reflection-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.reflection-label {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.reflection-textarea {
  width: 100%;
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  font-family: var(--font-family-base);
  font-size: 0.94rem;
  line-height: 1.55;
  color: var(--text-primary);
  resize: vertical;
}

.reflection-textarea:focus {
  outline: none;
  border-color: var(--color-secondary);
}

.feedback-panel {
  margin-top: var(--space-5);
  padding: var(--space-5);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--color-success);
  background-color: var(--color-success-soft);
}

.feedback-panel.feedback-explore {
  border-left-color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

.feedback-panel h3 {
  margin-bottom: var(--space-2);
}

.feedback-panel p {
  margin-bottom: var(--space-3);
}

.activity-submit-bar {
  margin-top: var(--space-5);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}
</style>

