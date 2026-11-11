import api from './api'

export const activityService = {
  async getActivity(activityId) {
    const response = await api.get(`/activities/${activityId}/`)
    return response.data.data
  },

  async submitAttempt(activityId, payload) {
    const response = await api.post(`/activities/${activityId}/attempts/`, payload)
    return response.data.data
  },
}

