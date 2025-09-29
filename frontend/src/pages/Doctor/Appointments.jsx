import React from 'react'
import { Calendar, User, Clock } from 'lucide-react'
import { useQuery } from "@tanstack/react-query";
import { appointmentsAPI } from '../../services'

const DoctorAppointments = () => {
  const { data: appointments, isLoading, error } = useQuery(
    'doctor-appointments',
    appointmentsAPI.list
  )

  if (isLoading) return <div>Loading appointments...</div>
  if (error) return <div>Error loading appointments: {error.message}</div>

  const todayAppointments = appointments?.data?.filter(apt => 
    new Date(apt.date).toDateString() === new Date().toDateString()
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <Calendar className="mr-2" size={24} />
          My Appointments
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Today's Appointments</h2>
            <div className="space-y-4">
              {todayAppointments?.map((appointment) => (
                <div key={appointment.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <User className="text-gray-400" size={20} />
                      <div>
                        <h3 className="font-medium text-gray-800">{appointment.patient?.name}</h3>
                        <p className="text-sm text-gray-600">{appointment.patient?.phone}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center space-x-1 text-sm text-gray-600">
                        <Clock size={14} />
                        <span>{appointment.time}</span>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                        appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {appointment.status}
                      </span>
                    </div>
                  </div>
                  <div className="mt-3 flex space-x-2">
                    <button className="btn-primary text-sm">
                      Start Consultation
                    </button>
                    <button className="btn-secondary text-sm">
                      View History
                    </button>
                  </div>
                </div>
              ))}
              {(!todayAppointments || todayAppointments.length === 0) && (
                <p className="text-gray-500 text-center py-8">No appointments scheduled for today</p>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Upcoming Appointments</h2>
            <div className="space-y-3">
              {appointments?.data?.slice(0, 5).map((appointment) => (
                <div key={appointment.id} className="border-b pb-3 last:border-b-0">
                  <p className="font-medium text-gray-800">{appointment.patient?.name}</p>
                  <p className="text-sm text-gray-600">
                    {new Date(appointment.date).toLocaleDateString()} at {appointment.time}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DoctorAppointments