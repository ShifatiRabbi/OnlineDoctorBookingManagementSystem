import api from './api'

export const doctorsAPI = {
  // Get full list of doctors
  list: async () => {
    const response = await api.get('/doctors/doctors/list/')
    return response.data
  },

  // Create new doctor
  create: async (doctorData) => {
    const response = await api.post('/doctors/doctors/', doctorData)
    return response.data
  },

  // Get single doctor by ID
  get: async (doctorId) => {
    const response = await api.get(`/doctors/doctors/${doctorId}/`)
    return response.data
  },

  // Update doctor by ID
  update: async (doctorId, doctorData) => {
    const response = await api.put(`/doctors/doctors/${doctorId}/`, doctorData)
    return response.data
  },

  // Create doctor schedule
  createSchedule: async (doctorId, scheduleData) => {
    const response = await api.post(`/doctors/doctors/${doctorId}/schedule/`, scheduleData)
    return response.data
  },

  // Get all schedules for doctor
  getSchedules: async (doctorId) => {
    const response = await api.get(`/doctors/doctors/${doctorId}/schedules/`)
    return response.data
  },
}
