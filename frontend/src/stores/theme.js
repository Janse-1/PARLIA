import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import logoLight from '../assets/fondo_claro.jpeg'
import logoDark from '../assets/fondo_oscuro.jpeg'

const THEME_STORAGE_KEY = 'parlia_theme'

function resolveInitialTheme() {
  try {
    const saved = localStorage.getItem(THEME_STORAGE_KEY)
    if (saved === 'dark' || saved === 'light') {
      return saved
    }
    if (
      typeof window !== 'undefined' &&
      window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches
    ) {
      return 'dark'
    }
  } catch {
    // Fallback seguro
  }
  return 'light'
}

function applyThemeToDOM(themeValue) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  if (themeValue === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
}

export const useThemeStore = defineStore('theme', () => {
  const mode = ref(resolveInitialTheme())
  applyThemeToDOM(mode.value)

  const isDark = computed(() => mode.value === 'dark')
  const brandLogo = computed(() => (isDark.value ? logoDark : logoLight))

  function setTheme(newMode) {
    mode.value = newMode === 'dark' ? 'dark' : 'light'
    try {
      localStorage.setItem(THEME_STORAGE_KEY, mode.value)
    } catch {
      // Sin bloqueo
    }
    applyThemeToDOM(mode.value)
  }

  function toggleTheme() {
    setTheme(isDark.value ? 'light' : 'dark')
  }

  return {
    mode,
    isDark,
    brandLogo,
    setTheme,
    toggleTheme,
  }
})
