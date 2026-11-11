<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
  isMobileOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close-mobile', 'expand-sidebar'])
const route = useRoute()
const isCareersOpen = ref(true)

const careers = [
  { key: 'Sistemas', label: 'Ing. de Sistemas' },
  { key: 'Industrial', label: 'Ing. Industrial' },
  { key: 'Mecanica', label: 'Ing. Mecánica' },
  { key: 'Civil', label: 'Ing. Civil' },
  { key: 'Ambiental', label: 'Ing. Ambiental' },
  { key: 'Energias', label: 'Ing. en Energías' },
]

function toggleCareers() {
  if (props.isCollapsed) {
    emit('expand-sidebar')
    isCareersOpen.value = true
  } else {
    isCareersOpen.value = !isCareersOpen.value
  }
}

function handleNavigate() {
  emit('close-mobile')
}
</script>

<template>
  <div>
    <div
      v-if="isMobileOpen"
      class="sidebar-backdrop"
      @click="emit('close-mobile')"
    />

    <aside
      class="sidebar"
      :class="{
        collapsed: isCollapsed,
        'mobile-open': isMobileOpen,
      }"
      aria-label="Menú lateral de recursos y carreras"
    >
      <div class="sidebar-scroll">
        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">APRENDIZAJE</span>

          <router-link
            to="/modules"
            class="sidebar-link"
            :class="{ active: route.path.startsWith('/modules') || route.path.startsWith('/lessons') }"
            title="Módulos del Laboratorio"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">Módulos (6 Ejes)</span>
          </router-link>
        </div>

        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">CONTEXTO POR PROGRAMA</span>

          <button
            type="button"
            class="sidebar-link accordion-btn"
            :class="{ active: route.path.startsWith('/careers') }"
            title="Carreras de Ingeniería"
            @click="toggleCareers"
          >
            <div class="accordion-left">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
              <span v-if="!isCollapsed" class="link-text">Carreras</span>
            </div>
            <svg
              v-if="!isCollapsed"
              class="chevron-icon"
              :class="{ rotated: isCareersOpen }"
              viewBox="0 0 24 24"
              width="16"
              height="16"
              stroke="currentColor"
              stroke-width="2"
              fill="none"
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>

          <ul v-if="!isCollapsed && isCareersOpen" class="submenu-list">
            <li v-for="career in careers" :key="career.key">
              <router-link
                :to="`/careers/${career.key}`"
                class="submenu-link"
                :class="{ active: route.params.program === career.key }"
                @click="handleNavigate"
              >
                <span class="submenu-dot" />
                <span>{{ career.label }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">CÁPSULAS DE CONSULTA LIBRE</span>

          <router-link
            to="/capsules/images"
            class="sidebar-link"
            :class="{ active: route.path === '/capsules/images' }"
            title="Cápsula: Imágenes Generativas"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <polyline points="21 15 16 10 5 21" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">Imágenes</span>
          </router-link>

          <router-link
            to="/capsules/writing"
            class="sidebar-link"
            :class="{ active: route.path === '/capsules/writing' }"
            title="Cápsula: Redacción Técnica"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">Redacción</span>
          </router-link>

          <router-link
            to="/prompts"
            class="sidebar-link"
            :class="{ active: route.path === '/prompts' }"
            title="Biblioteca de Prompts"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="4 17 10 11 4 5" />
              <line x1="12" y1="19" x2="20" y2="19" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">Prompts</span>
          </router-link>
        </div>
      </div>

      <div v-if="!isCollapsed" class="sidebar-footer">
        <p class="footer-note">
          Espacio formativo no punitivo. Las cápsulas de apoyo no alteran tu porcentaje de progreso.
        </p>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: var(--topbar-height);
  left: 0;
  bottom: 0;
  width: var(--sidebar-expanded-width);
  background-color: var(--bg-surface);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: width var(--transition-normal), transform var(--transition-normal);
  z-index: 40;
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4) var(--space-3);
}

.sidebar-section {
  margin-bottom: var(--space-5);
}

.section-heading {
  display: block;
  padding: 0 var(--space-3);
  margin-bottom: var(--space-2);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--text-secondary);
}

.sidebar-link {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.9rem;
  font-weight: 500;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.sidebar.collapsed .sidebar-link {
  justify-content: center;
  padding: 12px 0;
}

.sidebar-link:hover {
  background-color: var(--bg-subtle);
  color: var(--color-secondary);
}

.sidebar-link.active {
  background-color: var(--color-secondary-soft);
  color: var(--color-secondary-hover);
  font-weight: 600;
}

.accordion-btn {
  justify-content: space-between;
}

.accordion-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.chevron-icon {
  transition: transform var(--transition-fast);
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.submenu-list {
  list-style: none;
  margin-top: var(--space-1);
  padding-left: var(--space-4);
}

.submenu-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 7px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.84rem;
  color: var(--text-secondary);
  transition: color var(--transition-fast), background-color var(--transition-fast);
}

.submenu-link:hover {
  color: var(--text-primary);
  background-color: var(--bg-subtle);
}

.submenu-link.active {
  color: var(--color-primary-hover);
  background-color: var(--color-primary-soft);
  font-weight: 600;
}

.submenu-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
}

.footer-note {
  margin: 0;
  font-size: 0.76rem;
  line-height: 1.45;
  color: var(--text-secondary);
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 767px) {
  .sidebar {
    width: var(--sidebar-expanded-width);
    transform: translateX(-100%);
    box-shadow: var(--shadow-elevated);
  }

  .sidebar.collapsed {
    width: var(--sidebar-expanded-width);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: var(--topbar-height) 0 0 0;
    background-color: rgba(17, 24, 39, 0.45);
    z-index: 35;
  }
}
</style>

