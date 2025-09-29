import React, { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/auth'
import { useNotification } from '../hooks/useNotification'

const AuthContext = createContext()

// export const useAuth = () => {
//   const context = useContext(AuthContext)
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider')
//   }
//   return context
// }

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const { showError, showSuccess } = useNotification()

  useEffect(() => {
    if (token) {
      verifyToken()
    } else {
      setLoading(false)
    }
  }, [token])

  const verifyToken = async () => {
    try {
      const userData = await authAPI.verifyToken()
      setUser(userData)
    } catch (error) {
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials) => {
    try {
      setLoading(true)
      const response = await authAPI.login(credentials)
      const { token: newToken, user: userData } = response
      
      setToken(newToken)
      setUser(userData)
      localStorage.setItem('token', newToken)
      
      showSuccess('Login successful!')
      return { success: true }
    } catch (error) {
      showError(error.response?.data?.error || 'Login failed')
      return { success: false, error: error.response?.data?.error }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    showSuccess('Logged out successfully')
  }

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
    hasRole: (role) => user?.role === role,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}