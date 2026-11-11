<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useI18nStore } from '../stores/i18n'
import { useAuthStore } from '../stores/auth'

defineProps({
  isSidebarCollapsed: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle-sidebar'])
const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()
const i18nStore = useI18nStore()
const authStore = useAuthStore()

const searchQuery = ref('')

const navItems = computed(() => [
  { name: i18nStore.t.topbar.videos, path: '/videos', icon: 'video' },
  { name: i18nStore.t.topbar.news, path: '/news', icon: 'news' },
  { name: i18nStore.t.topbar.progress, path: '/progress', icon: 'progress' },
  { name: i18nStore.t.topbar.profile, path: '/profile', icon: 'profile' },
])

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
        :aria-label="i18nStore.t.topbar.toggleSidebar"
        @click="emit('toggle-sidebar')"
      >
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      <!-- T8.5.1: Logotipo Oficial Dinámico con Retorno al Inicio `/` -->
      <router-link to="/" class="brand-logo-link" title="Volver al Portal Principal ParLIA">
        <img
          :src="themeStore.brandLogo"
          alt="ParLIA - Educación e Inteligencia Artificial"
          class="brand-official-img"
        />
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
        :placeholder="i18nStore.t.topbar.searchPlaceholder"
        :aria-label="i18nStore.t.topbar.searchPlaceholder"
      />
    </form>

    <div class="topbar-right">
      <!-- T8.4.1: Selector de Idioma ES | EN -->
      <div class="lang-switch" role="group" aria-label="Selector de idioma">
        <button
          type="button"
          class="lang-btn"
          :class="{ active: i18nStore.locale === 'ES' }"
          @click="i18nStore.setLocale('ES')"
        >
          ES
        </button>
        <button
          type="button"
          class="lang-btn"
          :class="{ active: i18nStore.locale === 'EN' }"
          @click="i18nStore.setLocale('EN')"
        >
          EN
        </button>
      </div>

      <!-- T8.3.2: Switch de Tema Claro / Oscuro -->
      <button
        type="button"
        class="theme-toggle-btn"
        :title="themeStore.isDark ? i18nStore.t.topbar.lightMode : i18nStore.t.topbar.darkMode"
        :aria-label="themeStore.isDark ? i18nStore.t.topbar.lightMode : i18nStore.t.topbar.darkMode"
        @click="themeStore.toggleTheme()"
      >
        <!-- Sol (para cambiar a modo claro cuando está oscuro) -->
        <svg v-if="themeStore.isDark" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
        <!-- Luna (para cambiar a modo oscuro cuando está claro) -->
        <svg v-else viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      </button>

      <!-- Navegación rápida autenticada o botones Login/Registro -->
      <nav v-if="authStore.isAuthenticated" class="topbar-nav" aria-label="Navegación rápida superior">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="topbar-nav-link"
          :class="{ active: route.path.startsWith(item.path) }"
          :title="item.name"
        >
          <svg v-if="item.icon === 'video'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="4" width="20" height="16" rx="2" />
            <polygon points="10 9 15 12 10 15 10 9" />
          </svg>
          <svg v-else-if="item.icon === 'news'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
            <path d="M18 14h-8" />
            <path d="M15 18h-5" />
            <path d="M10 6h8v4h-8V6Z" />
          </svg>
          <svg v-else-if="item.icon === 'progress'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
          <svg v-else-if="item.icon === 'profile'" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span class="nav-label">{{ item.name }}</span>
        </router-link>
      </nav>

      <div v-else class="topbar-guest-actions">
        <router-link to="/login" class="btn btn-outline btn-sm">
          {{ i18nStore.t.topbar.login }}
        </router-link>
        <router-link to="/register" class="btn btn-primary btn-sm">
          {{ i18nStore.t.topbar.register }}
        </router-link>
      </div>
    </div>
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

.sidebar-toggle-btn,
.theme-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-surface);
  color: var(--text-primary);
  cursor: pointer;
  transition: background-color var(--transition-fast), border-color var(--transition-fast), color var(--transition-fast);
}

.sidebar-toggle-btn:hover,
.theme-toggle-btn:hover {
  background-color: var(--bg-subtle);
  border-color: var(--color-secondary);
  color: var(--color-secondary);
}

.brand-logo-link {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  transition: transform var(--transition-fast);
}

.brand-logo-link:hover {
  transform: scale(1.03);
}

.brand-official-img {
  height: 38px;
  width: auto;
  border-radius: 4px;
  object-fit: contain;
  display: block;
}

.topbar-search {
  position: relative;
  flex: 1;
  max-width: 360px;
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
  height: 36px;
  padding: 0 12px 0 36px;
  border-radius: 4px;
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
  font-family: var(--font-family-base);
  font-size: 0.86rem;
  color: var(--text-primary);
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-secondary);
  background-color: var(--bg-surface);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.lang-switch {
  display: inline-flex;
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  overflow: hidden;
  background-color: var(--bg-app);
}

.lang-btn {
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font-family-mono);
  font-size: 0.74rem;
  font-weight: 700;
  padding: 6px 9px;
  cursor: pointer;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.lang-btn.active {
  background-color: var(--color-primary);
  color: #FFFFFF;
}

.topbar-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.topbar-nav-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 4px;
  font-size: 0.86rem;
  font-weight: 500;
  color: var(--text-secondary);
  border: 1px solid transparent;
  transition: background-color var(--transition-fast), color var(--transition-fast), border-color var(--transition-fast);
}

.topbar-nav-link:hover {
  background-color: var(--bg-subtle);
  color: var(--text-primary);
}

.topbar-nav-link.active {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
  border-color: rgba(255, 91, 38, 0.25);
  font-weight: 600;
}

.topbar-guest-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.82rem;
}

@media (max-width: 900px) {
  .topbar-search,
  .nav-label {
    display: none;
  }
}

@media (max-width: 767px) {
  .topbar {
    padding: 0 var(--space-3);
  }

  .brand-official-img {
    height: 32px;
  }

  .topbar-nav-link {
    padding: 7px 9px;
  }
}
</style>
