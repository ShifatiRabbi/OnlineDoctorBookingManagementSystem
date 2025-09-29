import React, { createContext, useContext, useState, useEffect } from 'react'
import { branchesAPI } from '../services/branches'

const AppContext = createContext()

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
}

export const AppProvider = ({ children }) => {
  const [branches, setBranches] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBranches()
  }, [])

  const loadBranches = async () => {
    try {
      const response = await branchesAPI.getAllBranches()
      if (response.success) {
        setBranches(response.data)
      }
    } catch (error) {
      console.error('Failed to load branches:', error)
    } finally {
      setLoading(false)
    }
  }

  const getBranchById = (id) => {
    return branches.find(branch => branch.id === id)
  }

  const value = {
    branches,
    loading,
    getBranchById,
    refreshBranches: loadBranches,
  }

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  )
}