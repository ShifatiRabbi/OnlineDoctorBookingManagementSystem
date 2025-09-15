import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useQuery, useMutation } from 'react-query'
import { prescriptionsAPI, patientsAPI } from '../../../services'
import { useNotification } from '../../../hooks/useNotification'

const PrescriptionForm = ({ appointment, onSuccess }) => {
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm()
  const [medicines, setMedicines] = useState([])
  const [tests, setTests] = useState([])
  const { showSuccess, showError } = useNotification()

  const { data: medicinesData } = useQuery('medicines', prescriptionsAPI.getMedicines)
  const { data: testsData } = useQuery('tests', prescriptionsAPI.getTests)

  const createPrescriptionMutation = useMutation(prescriptionsAPI.create, {
    onSuccess: (data) => {
      if (data.success) {
        showSuccess('Prescription created successfully!')
        onSuccess?.()
      } else {
        showError(data.error)
      }
    },
    onError: (error) => {
      showError(error.response?.data?.error || 'Failed to create prescription')
    }
  })

  const addMedicine = () => {
    setMedicines([...medicines, { medicine_id: '', dosage: '', duration: '', instructions: '' }])
  }

  const removeMedicine = (index) => {
    setMedicines(medicines.filter((_, i) => i !== index))
  }

  const addTest = () => {
    setTests([...tests, { test_id: '', notes: '' }])
  }

  const removeTest = (index) => {
    setTests(tests.filter((_, i) => i !== index))
  }

  const onSubmit = async (data) => {
    const prescriptionData = {
      appointment_id: appointment.id,
      items: medicines.filter(m => m.medicine_id),
      tests: tests.filter(t => t.test_id),
      advice: data.advice
    }
    
    await createPrescriptionMutation.mutateAsync(prescriptionData)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="bg-gray-50 p-4 rounded-md">
        <h3 className="text-lg font-medium text-gray-800">Patient Information</h3>
        <p className="text-gray-600">{appointment.patient.name} - {appointment.patient.phone}</p>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-800 mb-4">Medicines</h3>
        {medicines.map((medicine, index) => (
          <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4 p-4 border rounded-md">
            <select
              value={medicine.medicine_id}
              onChange={(e) => {
                const newMedicines = [...medicines]
                newMedicines[index].medicine_id = e.target.value
                setMedicines(newMedicines)
              }}
              className="px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">Select Medicine</option>
              {medicinesData?.data?.map((med) => (
                <option key={med.id} value={med.id}>{med.name}</option>
              ))}
            </select>
            
            <input
              type="text"
              placeholder="Dosage"
              value={medicine.dosage}
              onChange={(e) => {
                const newMedicines = [...medicines]
                newMedicines[index].dosage = e.target.value
                setMedicines(newMedicines)
              }}
              className="px-3 py-2 border border-gray-300 rounded-md"
            />
            
            <input
              type="text"
              placeholder="Duration"
              value={medicine.duration}
              onChange={(e) => {
                const newMedicines = [...medicines]
                newMedicines[index].duration = e.target.value
                setMedicines(newMedicines)
              }}
              className="px-3 py-2 border border-gray-300 rounded-md"
            />
            
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="Instructions"
                value={medicine.instructions}
                onChange={(e) => {
                  const newMedicines = [...medicines]
                  newMedicines[index].instructions = e.target.value
                  setMedicines(newMedicines)
                }}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
              />
              <button
                type="button"
                onClick={() => removeMedicine(index)}
                className="px-3 py-2 text-red-600 hover:text-red-800"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
        <button
          type="button"
          onClick={addMedicine}
          className="px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
        >
          Add Medicine
        </button>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-800 mb-4">Tests</h3>
        {tests.map((test, index) => (
          <div key={index} className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 p-4 border rounded-md">
            <select
              value={test.test_id}
              onChange={(e) => {
                const newTests = [...tests]
                newTests[index].test_id = e.target.value
                setTests(newTests)
              }}
              className="px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">Select Test</option>
              {testsData?.data?.map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
            
            <input
              type="text"
              placeholder="Notes"
              value={test.notes}
              onChange={(e) => {
                const newTests = [...tests]
                newTests[index].notes = e.target.value
                setTests(newTests)
              }}
              className="px-3 py-2 border border-gray-300 rounded-md"
            />
            
            <button
              type="button"
              onClick={() => removeTest(index)}
              className="px-3 py-2 text-red-600 hover:text-red-800"
            >
              Remove
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={addTest}
          className="px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50"
        >
          Add Test
        </button>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Advice</label>
        <textarea
          {...register('advice')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Medical advice for the patient"
        />
      </div>

      <button
        type="submit"
        disabled={createPrescriptionMutation.isLoading}
        className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {createPrescriptionMutation.isLoading ? 'Creating...' : 'Create Prescription'}
      </button>
    </form>
  )
}

export default PrescriptionForm