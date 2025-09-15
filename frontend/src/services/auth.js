import api from './api'

export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials)
    return response.data
  },

  logout: async () => {
    const response = await api.post('/auth/logout/')
    return response.data
  },

  verifyToken: async () => {
    const response = await api.get('/auth/verify/')
    return response.data
  },

  changePassword: async (passwords) => {
    const response = await api.post('/auth/change-password/', passwords)
    return response.data
  },
}