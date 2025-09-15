import { useState } from 'react'
import { useNotification } from './useNotification'

export const useApi = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const { showError } = useNotification()

  const callApi = async (apiCall, successMessage = null) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiCall()
      
      if (successMessage && response.success) {
        // showSuccess(successMessage) - You can add this if needed
      }
      
      return response
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'An error occurred'
      setError(errorMsg)
      showError(errorMsg)
      return { success: false, error: errorMsg }
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    callApi,
    clearError: () => setError(null),
  }
}