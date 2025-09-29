import React, { useState } from 'react'
import { Users, Search } from 'lucide-react'
import { useQuery } from "@tanstack/react-query";
import { patientsAPI } from '../../services'

const PatientSearch = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: patients, isLoading, error, refetch } = useQuery(
    ['patients', searchTerm],
    () => patientsAPI.search({ phone: searchTerm, name: searchTerm }),
    { enabled: false }
  )

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchTerm.length > 2) {
      refetch()
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <Users className="mr-2" size={24} />
          Patient Search
        </h1>
      </div>

      <div className="card p-6">
        <form onSubmit={handleSearch} className="flex space-x-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name or phone number..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <button type="submit" className="btn-primary">
            Search
          </button>
        </form>

        {isLoading && <div>Searching patients...</div>}
        {error && <div className="text-red-600">Error: {error.message}</div>}

        {patients?.data && (
          <div className="table-container">
            <table className="table">
              <thead className="table-head">
                <tr>
                  <th className="table-header">Name</th>
                  <th className="table-header">Phone</th>
                  <th className="table-header">Address</th>
                  <th className="table-header">Gender</th>
                  <th className="table-header">Date of Birth</th>
                  <th className="table-header">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {patients.data.map((patient) => (
                  <tr key={patient.id} className="table-row">
                    <td className="table-cell">{patient.name}</td>
                    <td className="table-cell">{patient.phone}</td>
                    <td className="table-cell">{patient.address}</td>
                    <td className="table-cell capitalize">{patient.gender}</td>
                    <td className="table-cell">
                      {patient.dob ? new Date(patient.dob).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="table-cell">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-800 text-sm">
                          View
                        </button>
                        <button className="text-green-600 hover:text-green-800 text-sm">
                          Book Appointment
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default PatientSearch