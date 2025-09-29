import api from './api'

export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/accounts/login/', credentials)
    return response.data
  },

  logout: async () => {
    const response = await api.post('/accounts/logout/')
    return response.data
  },

  verifyToken: async () => {
    const response = await api.get('/accounts/verify/')
    return response.data
  },

  changePassword: async (passwords) => {
    const response = await api.post('/accounts/change-password/', passwords)
    return response.data
  },
}