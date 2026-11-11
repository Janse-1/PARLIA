import api from './api'

export const authService = {
  async login(email, password) {
    const response = await api.post('/auth/login/', { email, password })
    return response.data.data
  },

  async register(payload) {
    const response = await api.post('/auth/register/', payload)
    return response.data.data
  },

  async logout() {
    const response = await api.post('/auth/logout/')
    return response.data.data
  },

  async getMe() {
    const response = await api.get('/me/')
    return response.data.data
  },
}
