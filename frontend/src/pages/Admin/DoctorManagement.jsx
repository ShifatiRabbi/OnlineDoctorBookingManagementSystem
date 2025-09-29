import React from 'react'
import { UserCog, Plus } from 'lucide-react'

const DoctorManagement = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <UserCog className="mr-2" size={24} />
          Doctor Management
        </h1>
        <button className="btn-primary flex items-center">
          <Plus size={16} className="mr-1" />
          Add Doctor
        </button>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-600">Doctor management content will go here.</p>
      </div>
    </div>
  )
}

export default DoctorManagement