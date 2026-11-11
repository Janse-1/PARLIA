import api from './api'

export const progressService = {
  async getMyProgress() {
    const response = await api.get('/progress/me/')
    return response.data.data
  },

  async upsertProgress(lessonId, status) {
    const response = await api.post('/progress/', {
      lesson_id: lessonId,
      status,
    })
    return response.data.data
  },
}

