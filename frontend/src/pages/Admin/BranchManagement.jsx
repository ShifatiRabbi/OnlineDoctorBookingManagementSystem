import React from 'react'
import { Building, Plus } from 'lucide-react'
import { useQuery } from "@tanstack/react-query";
import { branchesAPI } from '../../services'

const BranchManagement = () => {
  const { data: branches, isLoading, error } = useQuery('branches', branchesAPI.getAllBranches)

  if (isLoading) return <div>Loading branches...</div>
  if (error) return <div>Error loading branches: {error.message}</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <Building className="mr-2" size={24} />
          Branch Management
        </h1>
        <button className="btn-primary flex items-center">
          <Plus size={16} className="mr-1" />
          Add Branch
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {branches?.data?.map((branch) => (
          <div key={branch.id} className="card p-6">
            <h3 className="text-lg font-semibold text-gray-800">{branch.name}</h3>
            <p className="text-gray-600 mt-2">{branch.address}</p>
            <p className="text-gray-600">{branch.phones}</p>
            <div className="mt-4 flex space-x-2">
              <button className="btn-secondary text-sm">
                Edit
              </button>
              <button className="btn-danger text-sm">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default BranchManagement