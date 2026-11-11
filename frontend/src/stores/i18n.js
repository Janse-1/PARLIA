import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const LANG_STORAGE_KEY = 'parlia_lang'

const messages = {
  ES: {
    topbar: {
      searchPlaceholder: 'Buscar módulos o temas...',
      videos: 'Videos',
      news: 'Noticias',
      progress: 'Progreso',
      profile: 'Perfil',
      login: 'Iniciar Sesión',
      register: 'Registro',
      lightMode: 'Cambiar a modo claro',
      darkMode: 'Cambiar a modo oscuro',
      toggleSidebar: 'Alternar menú lateral',
    },
    sidebar: {
      learningSection: 'APRENDIZAJE',
      modulesLink: 'Módulos (6 Ejes)',
      programsSection: 'CONTEXTO POR PROGRAMA',
      careersLabel: 'Carreras',
      capsulesSection: 'CÁPSULAS DE CONSULTA LIBRE',
      imagesLink: 'Imágenes',
      writingLink: 'Redacción',
      promptsLink: 'Prompts',
      suggestionsSection: 'COMUNIDAD Y MEJORA',
      suggestionsLink: 'Sugerencias',
      footerNote:
        'Espacio formativo no punitivo. Las cápsulas de apoyo no alteran tu porcentaje de progreso.',
      programs: {
        Sistemas: 'Ing. de Sistemas',
        Industrial: 'Ing. Industrial',
        Mecanica: 'Ing. Mecánica',
        Civil: 'Ing. Civil',
        Ambiental: 'Ing. Ambiental',
        Energias: 'Ing. en Energías',
      },
    },
    status: {
      completed: 'Completado',
      active: 'En Curso',
      locked: 'Pendiente',
    },
  },
  EN: {
    topbar: {
      searchPlaceholder: 'Search modules or topics...',
      videos: 'Videos',
      news: 'News',
      progress: 'Progress',
      profile: 'Profile',
      login: 'Sign In',
      register: 'Register',
      lightMode: 'Switch to light mode',
      darkMode: 'Switch to dark mode',
      toggleSidebar: 'Toggle sidebar menu',
    },
    sidebar: {
      learningSection: 'LEARNING PATH',
      modulesLink: 'Modules (6 Axes)',
      programsSection: 'PROGRAM CONTEXT',
      careersLabel: 'Programs',
      capsulesSection: 'OPEN REFERENCE CAPSULES',
      imagesLink: 'Images',
      writingLink: 'Technical Writing',
      promptsLink: 'Prompt Library',
      suggestionsSection: 'COMMUNITY & FEEDBACK',
      suggestionsLink: 'Suggestions',
      footerNote:
        'Non-punitive formative space. Reference capsules do not alter your progress percentage.',
      programs: {
        Sistemas: 'Systems Eng.',
        Industrial: 'Industrial Eng.',
        Mecanica: 'Mechanical Eng.',
        Civil: 'Civil Eng.',
        Ambiental: 'Environmental Eng.',
        Energias: 'Energy Eng.',
      },
    },
    status: {
      completed: 'Completed',
      active: 'In Progress',
      locked: 'Pending',
    },
  },
}

export const useI18nStore = defineStore('i18n', () => {
  const locale = ref(localStorage.getItem(LANG_STORAGE_KEY) || 'ES')

  const t = computed(() => messages[locale.value] || messages.ES)

  function setLocale(newLocale) {
    const normalized = newLocale === 'EN' ? 'EN' : 'ES'
    locale.value = normalized
    try {
      localStorage.setItem(LANG_STORAGE_KEY, normalized)
    } catch {
      // Sin bloqueo
    }
  }

  return {
    locale,
    t,
    setLocale,
  }
})
