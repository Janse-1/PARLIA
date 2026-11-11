import api from './api'

export const learningService = {
  async getModules() {
    const response = await api.get('/modules/')
    return response.data.data
  },

  async getModuleDetail(moduleId) {
    const response = await api.get(`/modules/${moduleId}/`)
    return response.data.data
  },

  async getLessonDetail(lessonId) {
    const response = await api.get(`/lessons/${lessonId}/`)
    return response.data.data
  },
}

