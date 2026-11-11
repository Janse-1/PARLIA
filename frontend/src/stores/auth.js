import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '../services/authService'
import { getStoredToken, setStoredToken } from '../services/api'

const USER_STORAGE_KEY = 'parlia_auth_user'

function getStoredUser() {
  try {
    const raw = sessionStorage.getItem(USER_STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function setStoredUser(userObj) {
  if (userObj) {
    sessionStorage.setItem(USER_STORAGE_KEY, JSON.stringify(userObj))
  } else {
    sessionStorage.removeItem(USER_STORAGE_KEY)
  }
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(getStoredToken())
  const user = ref(getStoredUser())
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => Boolean(token.value))

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const data = await authService.login(email, password)
      token.value = data.token
      user.value = data.user
      setStoredToken(data.token)
      setStoredUser(data.user)
      return data
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        'Credenciales inválidas. Verifica tu correo institucional y contraseña.'
      error.value = msg
      throw new Error(msg)
    } finally {
      loading.value = false
    }
  }

  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const data = await authService.register(payload)
      token.value = data.token
      user.value = data.user
      setStoredToken(data.token)
      setStoredUser(data.user)
      return data
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        'No fue posible completar el registro. Verifica los datos ingresados.'
      error.value = msg
      throw new Error(msg)
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    if (!token.value) return null
    loading.value = true
    try {
      const profile = await authService.getMe()
      user.value = profile
      setStoredUser(profile)
      return profile
    } catch (err) {
      if (err.response?.status === 401) {
        clearSession()
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      if (token.value) {
        await authService.logout()
      }
    } catch {
      // Incluso si el servidor falla al revocar, limpiamos la sesión local
    } finally {
      clearSession()
    }
  }

  function clearSession() {
    token.value = null
    user.value = null
    error.value = null
    setStoredToken(null)
    setStoredUser(null)
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    fetchMe,
    logout,
    clearSession,
  }
})
