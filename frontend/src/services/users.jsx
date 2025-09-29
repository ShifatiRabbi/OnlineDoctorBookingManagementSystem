import api from './api'

export const usersAPI = {
  list: async () => {
    const response = await api.get('/accounts/users/list/')
    return response.data
  },

  create: async (userData) => {
    const response = await api.post('/accounts/users/', userData)
    return response.data
  },

  update: async (userId, userData) => {
    const response = await api.put(`/accounts/users/${userId}/`, userData)
    return response.data
  },

  delete: async (userId) => {
    const response = await api.delete(`/accounts/users/${userId}/delete/`)
    return response.data
  },
}