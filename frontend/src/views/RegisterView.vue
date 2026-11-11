<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProgressStore } from '../stores/progress'

const router = useRouter()
const authStore = useAuthStore()
const progressStore = useProgressStore()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const program = ref('Sistemas')
const password = ref('')
const passwordConfirm = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const programs = [
  { value: 'Sistemas', label: 'Ingeniería de Sistemas' },
  { value: 'Industrial', label: 'Ingeniería Industrial' },
  { value: 'Mecanica', label: 'Ingeniería Mecánica' },
  { value: 'Civil', label: 'Ingeniería Civil' },
  { value: 'Ambiental', label: 'Ingeniería Ambiental' },
  { value: 'Energias', label: 'Ingeniería en Energías' },
  { value: 'Otro', label: 'Otro Programa' },
]

async function handleRegister() {
  errorMessage.value = ''

  if (!firstName.value.trim() || !lastName.value.trim() || !email.value.trim() || !password.value) {
    errorMessage.value = 'Por favor completa todos los campos obligatorios.'
    return
  }

  if (password.value !== passwordConfirm.value) {
    errorMessage.value = 'Las contraseñas no coinciden.'
    return
  }

  isSubmitting.value = true
  try {
    await authStore.register({
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      email: email.value.trim(),
      program: program.value,
      password: password.value,
      password_confirm: passwordConfirm.value,
    })
    await progressStore.fetchMyProgress().catch(() => null)
    router.push('/modules')
  } catch (err) {
    errorMessage.value = err.message || 'No fue posible completar el registro.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="card register-card">
    <div class="register-header">
      <router-link to="/" class="back-home-link">← Volver al Portal ParLIA</router-link>
      <h1>Registro de Estudiante</h1>
      <p class="subtitle">
        Crea tu cuenta en el Laboratorio Virtual de Aprendizaje en IA Generativa — Universidad de La Guajira.
      </p>
    </div>

    <form class="register-form" @submit.prevent="handleRegister">
      <div class="form-row-2">
        <div class="form-group">
          <label for="firstName">Nombres</label>
          <input
            id="firstName"
            v-model="firstName"
            type="text"
            class="form-input"
            placeholder="Ej. Carlos Andrés"
            required
          />
        </div>

        <div class="form-group">
          <label for="lastName">Apellidos</label>
          <input
            id="lastName"
            v-model="lastName"
            type="text"
            class="form-input"
            placeholder="Ej. Epiayú"
            required
          />
        </div>
      </div>

      <div class="form-group">
        <label for="regEmail">Correo Electrónico (Institucional o Personal)</label>
        <input
          id="regEmail"
          v-model="email"
          type="email"
          class="form-input"
          placeholder="usuario@uniguajira.edu.co"
          required
          autocomplete="email"
        />
      </div>

      <div class="form-group">
        <label for="program">Programa Académico</label>
        <select id="program" v-model="program" class="form-input">
          <option v-for="p in programs" :key="p.value" :value="p.value">
            {{ p.label }}
          </option>
        </select>
      </div>

      <div class="form-row-2">
        <div class="form-group">
          <label for="regPassword">Contraseña</label>
          <input
            id="regPassword"
            v-model="password"
            type="password"
            class="form-input"
            placeholder="Mínimo 8 caracteres"
            required
            autocomplete="new-password"
          />
        </div>

        <div class="form-group">
          <label for="regPasswordConfirm">Confirmar Contraseña</label>
          <input
            id="regPasswordConfirm"
            v-model="passwordConfirm"
            type="password"
            class="form-input"
            placeholder="Repite la contraseña"
            required
            autocomplete="new-password"
          />
        </div>
      </div>

      <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>

      <button type="submit" class="btn btn-primary register-btn" :disabled="isSubmitting">
        {{ isSubmitting ? 'Creando cuenta...' : 'Crear Cuenta e Ingresar' }}
      </button>

      <p class="auth-switch-text">
        ¿Ya tienes una cuenta?
        <router-link to="/login">Inicia sesión aquí</router-link>
      </p>
    </form>
  </div>
</template>

<style scoped>
.register-card {
  width: 100%;
  max-width: 520px;
  padding: var(--space-8);
}

.back-home-link {
  display: inline-block;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-secondary);
  margin-bottom: var(--space-3);
}

.subtitle {
  font-size: 0.88rem;
  color: var(--text-secondary);
  margin-top: var(--space-1);
  margin-bottom: 0;
}

.register-form {
  display: grid;
  gap: var(--space-4);
  margin-top: var(--space-5);
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-primary);
}

.form-input {
  height: 40px;
  padding: 0 12px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  font-family: var(--font-family-base);
  font-size: 0.9rem;
  color: var(--text-primary);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-secondary);
}

.error-banner {
  margin: 0;
  padding: var(--space-3);
  border-radius: 4px;
  background-color: var(--color-accent-soft);
  color: var(--color-accent-hover);
  font-size: 0.84rem;
  font-weight: 500;
}

.register-btn {
  width: 100%;
  height: 42px;
}

.auth-switch-text {
  margin: 0;
  text-align: center;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

@media (max-width: 560px) {
  .form-row-2 {
    grid-template-columns: 1fr;
  }
}
</style>
