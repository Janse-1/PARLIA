import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ModulesView from '../views/ModulesView.vue'
import ModuleDetailView from '../views/ModuleDetailView.vue'
import LessonDetailView from '../views/LessonDetailView.vue'
import ProgressView from '../views/ProgressView.vue'
import VideosView from '../views/VideosView.vue'
import NewsView from '../views/NewsView.vue'
import ProfileView from '../views/ProfileView.vue'
import CareerCasesView from '../views/CareerCasesView.vue'
import ImagesCapsuleView from '../views/ImagesCapsuleView.vue'
import WritingCapsuleView from '../views/WritingCapsuleView.vue'
import PromptsLibraryView from '../views/PromptsLibraryView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { layout: 'landing', public: true },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { layout: 'auth', public: true, guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { layout: 'auth', public: true, guestOnly: true },
  },
  {
    path: '/modules',
    name: 'modules',
    component: ModulesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/modules/:id',
    name: 'module-detail',
    component: ModuleDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/lessons/:id',
    name: 'lesson-detail',
    component: LessonDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: '/progress',
    name: 'progress',
    component: ProgressView,
    meta: { requiresAuth: true },
  },
  {
    path: '/videos',
    name: 'videos',
    component: VideosView,
    meta: { requiresAuth: true },
  },
  {
    path: '/news',
    name: 'news',
    component: NewsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: '/careers/:program',
    name: 'career-cases',
    component: CareerCasesView,
    meta: { requiresAuth: true },
  },
  {
    path: '/capsules/images',
    name: 'capsule-images',
    component: ImagesCapsuleView,
    meta: { requiresAuth: true },
  },
  {
    path: '/capsules/writing',
    name: 'capsule-writing',
    component: WritingCapsuleView,
    meta: { requiresAuth: true },
  },
  {
    path: '/prompts',
    name: 'prompts-library',
    component: PromptsLibraryView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  // Antes de iniciar sesión NO se ve nada de módulos, carreras ni cápsulas internas
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  // Si ya tiene sesión activa y va a /login o /register, llevarlo a /modules
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'modules' }
  }

  return true
})

export default router
