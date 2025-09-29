import api from './api'

export const branchesAPI = {
  getAllBranches: async () => {
    const response = await api.get('/branches/list/')
    return response.data
  },

  create: async (branchData) => {
    const response = await api.post('/branches/', branchData)
    return response.data
  },

  update: async (branchId, branchData) => {
    const response = await api.put(`/branches/${branchId}/`, branchData)
    return response.data
  },

  delete: async (branchId) => {
    const response = await api.delete(`/branches/${branchId}/delete/`)
    return response.data
  },
}