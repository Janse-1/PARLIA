<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProgressStore } from '../stores/progress'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const progressStore = useProgressStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleSubmit() {
  errorMessage.value = ''
  if (!email.value.trim() || !password.value) {
    errorMessage.value = 'Por favor ingresa tu correo institucional y contraseña.'
    return
  }

  isSubmitting.value = true
  try {
    await authStore.login(email.value.trim(), password.value)
    await progressStore.fetchMyProgress()
    const target = route.query.redirect?.toString() || '/modules'
    router.push(target)
  } catch (err) {
    errorMessage.value = err.message || 'No fue posible iniciar sesión.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="card login-card">
    <div class="login-brand">
      <span class="brand-mark">P</span>
      <div>
        <h1>PARLIA</h1>
        <p class="brand-caption">Laboratorio Virtual de Aprendizaje en IA Generativa</p>
      </div>
    </div>

    <div class="callout">
      <strong>Entorno Formativo No Punitivo:</strong>
      Universidad de La Guajira - Facultad de Ingeniería. Experimenta, audita y fortalece tu criterio técnico sin calificaciones ni riesgos académicos.
    </div>

    <form class="login-form" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Correo Institucional</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="form-input"
          placeholder="usuario@uniguajira.edu.co"
          required
          autocomplete="email"
        />
      </div>

      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="form-input"
          placeholder="Ingresa tu contraseña"
          required
          autocomplete="current-password"
        />
      </div>

      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <button type="submit" class="btn btn-primary login-btn" :disabled="isSubmitting">
        {{ isSubmitting ? 'Verificando credenciales...' : 'Ingresar al Laboratorio' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.login-card {
  width: 100%;
  max-width: 440px;
  padding: var(--space-8);
}

.login-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background-color: var(--color-primary);
  color: var(--text-inverse);
  font-weight: 700;
  font-size: 1.35rem;
}

.brand-caption {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.login-form {
  display: grid;
  gap: var(--space-4);
  margin-top: var(--space-5);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--text-primary);
}

.form-input {
  height: 42px;
  padding: 0 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  font-family: var(--font-family-base);
  font-size: 0.92rem;
  color: var(--text-primary);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-secondary);
}

.error-banner {
  margin: 0;
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  background-color: var(--color-accent-soft);
  color: var(--color-accent-hover);
  font-size: 0.85rem;
  font-weight: 500;
}

.login-btn {
  width: 100%;
  height: 44px;
}
</style>
