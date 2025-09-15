import api from './api'

export const prescriptionsAPI = {
  create: async (prescriptionData) => {
    const response = await api.post('/prescriptions/prescriptions/', prescriptionData)
    return response.data
  },

  get: async (prescriptionId) => {
    const response = await api.get(`/prescriptions/prescriptions/${prescriptionId}/`)
    return response.data
  },

  getPatientPrescriptions: async (patientId) => {
    const response = await api.get(`/prescriptions/patients/${patientId}/prescriptions/`)
    return response.data
  },

  getMedicines: async () => {
    const response = await api.get('/prescriptions/medicines/')
    return response.data
  },

  getTests: async () => {
    const response = await api.get('/prescriptions/tests/')
    return response.data
  },

  print: async (prescriptionId) => {
    const response = await api.get(`/prescriptions/prescriptions/${prescriptionId}/print/`)
    return response.data
  },
}