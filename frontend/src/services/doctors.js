import api from './api'

export const doctorsAPI = {
  create: async (doctorData) => {
    const response = await api.post('/doctors/doctors/', doctorData)
    return response.data
  },

  get: async (doctorId) => {
    const response = await api.get(`/doctors/doctors/${doctorId}/`)
    return response.data
  },

  update: async (doctorId, doctorData) => {
    const response = await api.put(`/doctors/doctors/${doctorId}/`, doctorData)
    return response.data
  },

  list: async () => {
    const response = await api.get('/doctors/doctors/list/')
    return response.data
  },

  createSchedule: async (doctorId, scheduleData) => {
    const response = await api.post(`/doctors/doctors/${doctorId}/schedule/`, scheduleData)
    return response.data
  },

  getSchedules: async (doctorId) => {
    const response = await api.get(`/doctors/doctors/${doctorId}/schedules/`)
    return response.data
  },
}