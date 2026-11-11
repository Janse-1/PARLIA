<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProgressStore } from '../stores/progress'

const router = useRouter()
const authStore = useAuthStore()
const progressStore = useProgressStore()

onMounted(async () => {
  try {
    await authStore.fetchMe()
    await progressStore.fetchMyProgress()
  } catch {
    // Manejado por interceptor 401
  }
})

const studentProfile = computed(() => {
  const u = authStore.user || {}
  return {
    full_name: u.full_name || u.username || 'Estudiante Uniguajira',
    email: u.email || '',
    program_display: u.program_display || u.program || 'Facultad de Ingeniería',
    overall_percentage: progressStore.overallPercentage,
    completed_lessons: progressStore.completedLessons,
    total_lessons: progressStore.totalLessons,
  }
})

async function handleLogout() {
  await authStore.logout()
  progressStore.resetProgressState()
  router.push('/login')
}
</script>

<template>
  <section class="profile-view">
    <header class="view-header">
      <span class="badge badge-primary">Cuenta Institucional</span>
      <h1>Perfil del Estudiante</h1>
      <p class="subtitle">
        Universidad de La Guajira - Facultad de Ingeniería
      </p>
    </header>

    <div class="card profile-card">
      <div class="profile-details">
        <div class="detail-row">
          <span class="detail-label">Nombre Completo</span>
          <span class="detail-value">{{ studentProfile.full_name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Correo Institucional</span>
          <span class="detail-value">{{ studentProfile.email }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Programa Académico</span>
          <span class="detail-value">{{ studentProfile.program_display }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Lecciones Superadas</span>
          <span class="detail-value">
            {{ studentProfile.completed_lessons }} de {{ studentProfile.total_lessons }}
          </span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Avance Global en PARLIA</span>
          <span class="badge badge-success">{{ studentProfile.overall_percentage }}% Completado</span>
        </div>
      </div>

      <div class="profile-actions">
        <router-link to="/progress" class="btn btn-secondary">
          Ir a Mi Ruta de Progreso
        </router-link>
        <button type="button" class="btn btn-outline" @click="handleLogout">
          Cerrar Sesión
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  margin-bottom: var(--space-6);
}

.view-header h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

.profile-card {
  max-width: 640px;
}

.profile-details {
  display: grid;
  gap: var(--space-4);
}

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-subtle);
  gap: var(--space-4);
  flex-wrap: wrap;
}

.detail-label {
  font-size: 0.86rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.detail-value {
  font-weight: 600;
  color: var(--text-primary);
}

.profile-actions {
  margin-top: var(--space-6);
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}
</style>
