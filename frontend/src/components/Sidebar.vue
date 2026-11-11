<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '../stores/theme'
import { useI18nStore } from '../stores/i18n'

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
const themeStore = useThemeStore()
const i18nStore = useI18nStore()
const isCareersOpen = ref(true)

const careerKeys = ['Sistemas', 'Industrial', 'Mecanica', 'Civil', 'Ambiental', 'Energias']

const careers = computed(() =>
  careerKeys.map((key) => ({
    key,
    label: i18nStore.t.sidebar.programs[key] || key,
  }))
)

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
        <!-- T8.5.1: Logotipo Oficial Dinámico con retorno a `/` en el Sidebar -->
        <div v-if="!isCollapsed" class="sidebar-brand-box">
          <router-link to="/" class="sidebar-logo-link" @click="handleNavigate">
            <img
              :src="themeStore.brandLogo"
              alt="ParLIA Inicio"
              class="sidebar-brand-img"
            />
          </router-link>
        </div>

        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">{{ i18nStore.t.sidebar.learningSection }}</span>

          <router-link
            to="/modules"
            class="sidebar-link"
            :class="{ active: route.path.startsWith('/modules') || route.path.startsWith('/lessons') }"
            :title="i18nStore.t.sidebar.modulesLink"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.modulesLink }}</span>
          </router-link>
        </div>

        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">{{ i18nStore.t.sidebar.programsSection }}</span>

          <button
            type="button"
            class="sidebar-link accordion-btn"
            :class="{ active: route.path.startsWith('/careers') }"
            :title="i18nStore.t.sidebar.careersLabel"
            @click="toggleCareers"
          >
            <div class="accordion-left">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
              <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.careersLabel }}</span>
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
          <span v-if="!isCollapsed" class="section-heading">{{ i18nStore.t.sidebar.capsulesSection }}</span>

          <router-link
            to="/capsules/images"
            class="sidebar-link"
            :class="{ active: route.path === '/capsules/images' }"
            :title="i18nStore.t.sidebar.imagesLink"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <polyline points="21 15 16 10 5 21" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.imagesLink }}</span>
          </router-link>

          <router-link
            to="/capsules/writing"
            class="sidebar-link"
            :class="{ active: route.path === '/capsules/writing' }"
            :title="i18nStore.t.sidebar.writingLink"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.writingLink }}</span>
          </router-link>

          <router-link
            to="/prompts"
            class="sidebar-link"
            :class="{ active: route.path === '/prompts' }"
            :title="i18nStore.t.sidebar.promptsLink"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="4 17 10 11 4 5" />
              <line x1="12" y1="19" x2="20" y2="19" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.promptsLink }}</span>
          </router-link>
        </div>

        <div class="sidebar-section">
          <span v-if="!isCollapsed" class="section-heading">{{ i18nStore.t.sidebar.suggestionsSection }}</span>

          <a
            href="https://forms.gle/rLWN64RDtBjdeMbg7"
            target="_blank"
            rel="noopener noreferrer"
            class="sidebar-link"
            :title="i18nStore.t.sidebar.suggestionsLink"
            @click="handleNavigate"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            <span v-if="!isCollapsed" class="link-text">{{ i18nStore.t.sidebar.suggestionsLink }}</span>
          </a>
        </div>
      </div>

      <div v-if="!isCollapsed" class="sidebar-footer">
        <p class="footer-note">
          {{ i18nStore.t.sidebar.footerNote }}
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

.sidebar-brand-box {
  padding: 0 var(--space-2) var(--space-4);
  margin-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-subtle);
}

.sidebar-logo-link {
  display: inline-flex;
  cursor: pointer;
  transition: transform var(--transition-fast);
}

.sidebar-logo-link:hover {
  transform: scale(1.02);
}

.sidebar-brand-img {
  height: 36px;
  width: auto;
  border-radius: 4px;
  object-fit: contain;
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
  padding: 9px 12px;
  border-radius: 4px;
  color: var(--text-primary);
  font-size: 0.88rem;
  font-weight: 500;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  text-align: left;
  transition: background-color var(--transition-fast), color var(--transition-fast), border-color var(--transition-fast);
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
  color: var(--color-secondary);
  border-left: 3px solid var(--color-secondary);
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
  padding-left: var(--space-3);
  border-left: 1px solid var(--border-subtle);
  margin-left: var(--space-4);
}

.submenu-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 0.84rem;
  color: var(--text-secondary);
  transition: color var(--transition-fast), background-color var(--transition-fast);
}

.submenu-link:hover {
  color: var(--text-primary);
  background-color: var(--bg-subtle);
}

.submenu-link.active {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  font-weight: 600;
}

.submenu-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background-color: currentColor;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--border-subtle);
  background-color: var(--bg-subtle);
}

.footer-note {
  margin: 0;
  font-size: 0.74rem;
  line-height: 1.45;
  color: var(--text-secondary);
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 767px) {
  .sidebar {
    transform: translateX(-100%);
    width: var(--sidebar-expanded-width);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .sidebar-backdrop {
    display: block;
    position: fixed;
    top: var(--topbar-height);
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(12, 30, 47, 0.55);
    z-index: 35;
  }
}
</style>
