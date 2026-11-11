<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Topbar from '../components/Topbar.vue'
import Sidebar from '../components/Sidebar.vue'

const isSidebarCollapsed = ref(false)
const isMobileSidebarOpen = ref(false)

function updateResponsiveState() {
  const width = window.innerWidth
  if (width >= 768 && width < 1280) {
    isSidebarCollapsed.value = true
  } else if (width >= 1280) {
    isSidebarCollapsed.value = false
  }
}

function handleToggleSidebar() {
  if (window.innerWidth < 768) {
    isMobileSidebarOpen.value = !isMobileSidebarOpen.value
  } else {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }
}

onMounted(() => {
  updateResponsiveState()
  window.addEventListener('resize', updateResponsiveState)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateResponsiveState)
})
</script>

<template>
  <div class="app-shell">
    <Topbar
      :is-sidebar-collapsed="isSidebarCollapsed"
      @toggle-sidebar="handleToggleSidebar"
    />

    <Sidebar
      :is-collapsed="isSidebarCollapsed"
      :is-mobile-open="isMobileSidebarOpen"
      @close-mobile="isMobileSidebarOpen = false"
      @expand-sidebar="isSidebarCollapsed = false"
    />

    <main
      class="main-workspace"
      :class="{ 'sidebar-collapsed': isSidebarCollapsed }"
    >
      <div class="workspace-container">
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background-color: var(--bg-app);
}

.main-workspace {
  padding-top: var(--topbar-height);
  margin-left: var(--sidebar-expanded-width);
  min-height: 100vh;
  transition: margin-left var(--transition-normal);
}

.main-workspace.sidebar-collapsed {
  margin-left: var(--sidebar-collapsed-width);
}

.workspace-container {
  max-width: 1120px;
  margin: 0 auto;
  padding: var(--space-6) var(--space-6) var(--space-10);
}

@media (max-width: 767px) {
  .main-workspace,
  .main-workspace.sidebar-collapsed {
    margin-left: 0;
  }

  .workspace-container {
    padding: var(--space-4) var(--space-4) var(--space-8);
  }
}
</style>

