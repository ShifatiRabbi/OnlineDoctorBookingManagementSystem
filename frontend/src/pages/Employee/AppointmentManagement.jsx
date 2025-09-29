import React, { useState } from 'react'
import { Calendar, Plus, Search } from 'lucide-react'
import { useQuery } from "@tanstack/react-query";
import { appointmentsAPI } from '../../services'
import AppointmentForm from '../../components/employee/AppointmentManagement/AppointmentForm'

const AppointmentManagement = () => {
  const [showForm, setShowForm] = useState(false)
  const { data: appointments, isLoading, error } = useQuery(
    'appointments',
    appointmentsAPI.list
  )

  if (isLoading) return <div>Loading appointments...</div>
  if (error) return <div>Error loading appointments: {error.message}</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <Calendar className="mr-2" size={24} />
          Appointment Management
        </h1>
        <div className="flex space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Search appointments..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <button 
            className="btn-primary flex items-center"
            onClick={() => setShowForm(true)}
          >
            <Plus size={16} className="mr-1" />
            New Appointment
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card p-6">
          <AppointmentForm onSuccess={() => setShowForm(false)} />
        </div>
      )}

      <div className="card p-6">
        <div className="table-container">
          <table className="table">
            <thead className="table-head">
              <tr>
                <th className="table-header">Patient</th>
                <th className="table-header">Doctor</th>
                <th className="table-header">Date & Time</th>
                <th className="table-header">Branch</th>
                <th className="table-header">Status</th>
                <th className="table-header">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {appointments?.data?.map((appointment) => (
                <tr key={appointment.id} className="table-row">
                  <td className="table-cell">{appointment.patient?.name}</td>
                  <td className="table-cell">{appointment.doctor?.name}</td>
                  <td className="table-cell">
                    {new Date(appointment.date).toLocaleDateString()} at {appointment.time}
                  </td>
                  <td className="table-cell">{appointment.branch?.name}</td>
                  <td className="table-cell">
                    <span className={`px-2 py-1 text-xs rounded-full capitalize ${
                      appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                      appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      appointment.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {appointment.status}
                    </span>
                  </td>
                  <td className="table-cell">
                    <div className="flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-800 text-sm">
                        Edit
                      </button>
                      <button className="text-red-600 hover:text-red-800 text-sm">
                        Cancel
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default AppointmentManagement