import api from './api'

export const patientsAPI = {
  create: async (patientData) => {
    const response = await api.post('/patients/', patientData)
    return response.data
  },

  get: async (patientId) => {
    const response = await api.get(`/patients/${patientId}/details/`)
    return response.data
  },

  update: async (patientId, patientData) => {
    const response = await api.put(`/patients/${patientId}/`, patientData)
    return response.data
  },

  search: async (searchParams) => {
    const response = await api.get('/patients/search/', { params: searchParams })
    return response.data
  },

  getAppointments: async (patientId) => {
    const response = await api.get(`/patients/${patientId}/appointments/`)
    return response.data
  },

  getPrescriptions: async (patientId) => {
    const response = await api.get(`/patients/${patientId}/prescriptions/`)
    return response.data
  },
}