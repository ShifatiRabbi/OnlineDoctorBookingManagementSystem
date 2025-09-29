import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useQuery, useMutation } from "@tanstack/react-query"
import { patientsAPI, doctorsAPI, appointmentsAPI } from '../../../services'
import { useNotification } from '../../../hooks/useNotification'

const AppointmentForm = ({ onSuccess }) => {
  const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm()
  const [searchTerm, setSearchTerm] = useState('')
  const { showSuccess, showError } = useNotification()

  // Fetch doctors and patients
  const { data: doctorsData } = useQuery('doctors', doctorsAPI.list)
  const { data: patientsData, refetch: searchPatients } = useQuery(
    ['patients', searchTerm],
    () => patientsAPI.search({ phone: searchTerm, name: searchTerm }),
    { enabled: false }
  )

  const createAppointmentMutation = useMutation(appointmentsAPI.create, {
    onSuccess: (data) => {
      if (data.success) {
        showSuccess('Appointment created successfully!')
        onSuccess?.()
      } else {
        showError(data.error)
      }
    },
    onError: (error) => {
      showError(error.response?.data?.error || 'Failed to create appointment')
    }
  })

  const onSubmit = async (data) => {
    await createAppointmentMutation.mutateAsync(data)
  }

  const handlePatientSearch = (e) => {
    setSearchTerm(e.target.value)
    if (e.target.value.length > 2) {
      searchPatients()
    }
  }

  const selectPatient = (patient) => {
    setValue('patient_id', patient.id)
    setSearchTerm(patient.name)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Patient</label>
        <div className="relative mt-1">
          <input
            type="text"
            value={searchTerm}
            onChange={handlePatientSearch}
            placeholder="Search by name or phone"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          {patientsData?.data && patientsData.data.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg">
              {patientsData.data.map((patient) => (
                <div
                  key={patient.id}
                  className="px-4 py-2 cursor-pointer hover:bg-gray-100"
                  onClick={() => selectPatient(patient)}
                >
                  {patient.name} - {patient.phone}
                </div>
              ))}
            </div>
          )}
        </div>
        <input type="hidden" {...register('patient_id', { required: 'Patient is required' })} />
        {errors.patient_id && (
          <p className="mt-1 text-sm text-red-600">{errors.patient_id.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Doctor</label>
        <select
          {...register('doctor_id', { required: 'Doctor is required' })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Select Doctor</option>
          {doctorsData?.data?.map((doctor) => (
            <option key={doctor.id} value={doctor.id}>
              {doctor.name} - {doctor.specialties?.join(', ')}
            </option>
          ))}
        </select>
        {errors.doctor_id && (
          <p className="mt-1 text-sm text-red-600">{errors.doctor_id.message}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Date</label>
          <input
            type="date"
            {...register('date', { required: 'Date is required' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          {errors.date && (
            <p className="mt-1 text-sm text-red-600">{errors.date.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Time</label>
          <input
            type="time"
            {...register('time', { required: 'Time is required' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          {errors.time && (
            <p className="mt-1 text-sm text-red-600">{errors.time.message}</p>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Notes</label>
        <textarea
          {...register('notes')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Additional notes for the appointment"
        />
      </div>

      <button
        type="submit"
        disabled={createAppointmentMutation.isLoading}
        className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {createAppointmentMutation.isLoading ? 'Creating...' : 'Create Appointment'}
      </button>
    </form>
  )
}

export default AppointmentForm