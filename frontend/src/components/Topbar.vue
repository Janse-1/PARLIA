<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

defineProps({
  isSidebarCollapsed: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle-sidebar'])
const router = useRouter()
const route = useRoute()
const searchQuery = ref('')

const navItems = [
  { name: 'Videos', path: '/videos', icon: 'video' },
  { name: 'Noticias', path: '/news', icon: 'news' },
  { name: 'Progreso', path: '/progress', icon: 'progress' },
  { name: 'Perfil', path: '/profile', icon: 'profile' },
]

function handleSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  router.push({ path: '/modules', query: { q } })
}
</script>

<template>
  <header class="topbar">
    <div class="topbar-left">
      <button
        type="button"
        class="sidebar-toggle-btn"
        :aria-label="isSidebarCollapsed ? 'Expandir menú lateral' : 'Contraer menú lateral'"
        @click="emit('toggle-sidebar')"
      >
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <router-link to="/modules" class="brand-link">
        <span class="brand-mark">P</span>
        <div class="brand-text">
          <span class="brand-title">PARLIA</span>
          <span class="brand-subtitle">Uniguajira Ingeniería</span>
        </div>
      </router-link>
    </div>

    <form class="topbar-search" @submit.prevent="handleSearch">
      <svg class="search-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        v-model="searchQuery"
        type="search"
        class="search-input"
        placeholder="Buscar módulos o temas..."
        aria-label="Buscar módulos o temas"
      />
    </form>

    <nav class="topbar-nav" aria-label="Navegación rápida superior">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="topbar-nav-link"
        :class="{ active: route.path.startsWith(item.path) }"
        :title="item.name"
      >
        <!-- Icono Videos -->
        <svg v-if="item.icon === 'video'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="2" />
          <polygon points="10 9 15 12 10 15 10 9" />
        </svg>
        <!-- Icono Noticias -->
        <svg v-else-if="item.icon === 'news'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
          <path d="M18 14h-8" />
          <path d="M15 18h-5" />
          <path d="M10 6h8v4h-8V6Z" />
        </svg>
        <!-- Icono Progreso -->
        <svg v-else-if="item.icon === 'progress'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="m8 3 4 8 5-5 5 15H2L8 3z" />
        </svg>
        <!-- Icono Perfil -->
        <svg v-else-if="item.icon === 'profile'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span class="nav-label">{{ item.name }}</span>
      </router-link>
    </nav>
  </header>
</template>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--topbar-height);
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-5);
  z-index: 50;
  gap: var(--space-4);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.sidebar-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  color: var(--text-primary);
  cursor: pointer;
  transition: background-color var(--transition-fast), border-color var(--transition-fast);
}

.sidebar-toggle-btn:hover {
  background-color: var(--bg-subtle);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--text-primary);
}

.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  background-color: var(--color-primary);
  color: var(--text-inverse);
  font-weight: 700;
  font-size: 1.05rem;
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.brand-title {
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: 0.03em;
  color: var(--text-primary);
}

.brand-subtitle {
  font-size: 0.72rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.topbar-search {
  position: relative;
  flex: 1;
  max-width: 380px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-secondary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 38px;
  padding: 0 14px 0 36px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
  font-family: var(--font-family-base);
  font-size: 0.88rem;
  color: var(--text-primary);
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-secondary);
  background-color: var(--bg-surface);
}

.topbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.topbar-nav-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-secondary);
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.topbar-nav-link:hover {
  background-color: var(--bg-subtle);
  color: var(--text-primary);
}

.topbar-nav-link.active {
  background-color: var(--color-primary-soft);
  color: var(--color-primary-hover);
  font-weight: 600;
}

@media (max-width: 767px) {
  .topbar {
    padding: 0 var(--space-3);
  }

  .topbar-search,
  .brand-subtitle,
  .nav-label {
    display: none;
  }

  .topbar-nav-link {
    padding: 8px 10px;
  }
}
</style>

