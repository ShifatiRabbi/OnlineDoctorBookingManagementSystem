import api from './api'

export const appointmentsAPI = {
  create: async (appointmentData) => {
    const response = await api.post('/appointments/', appointmentData)
    return response.data
  },

  get: async (appointmentId) => {
    const response = await api.get(`/appointments/${appointmentId}/`)
    return response.data
  },

  update: async (appointmentId, appointmentData) => {
    const response = await api.put(`/appointments/${appointmentId}/`, appointmentData)
    return response.data
  },

  cancel: async (appointmentId) => {
    const response = await api.delete(`/appointments/${appointmentId}/`)
    return response.data
  },

  list: async (params = {}) => {
    const response = await api.get('/appointments/', { params })
    return response.data
  },

  getTimeSlots: async (doctorId, branchId, date) => {
    const response = await api.get(`/doctors/${doctorId}/branches/${branchId}/generate-slots/?date=${date}`)
    return response.data
  },
}