import React from 'react'
import { FileText } from 'lucide-react'

const DoctorPrescriptions = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <FileText className="mr-2" size={24} />
          Prescriptions
        </h1>
      </div>
      
      <div className="card p-6">
        <p className="text-gray-600">Prescription management content will go here.</p>
      </div>
    </div>
  )
}

export default DoctorPrescriptions