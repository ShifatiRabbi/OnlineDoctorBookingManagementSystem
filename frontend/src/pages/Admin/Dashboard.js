import React from 'react'
import { 
  Users, 
  Building, 
  Calendar, 
  FileText,
  DollarSign,
  TrendingUp
} from 'lucide-react'
import { useQuery } from 'react-query'
import { appointmentsAPI, usersAPI, branchesAPI } from '../../services'

const AdminDashboard = () => {
  const { data: stats } = useQuery('admin-stats', async () => {
    const [appointments, users, branches] = await Promise.all([
      appointmentsAPI.list(),
      usersAPI.list(),
      branchesAPI.getAllBranches()
    ])
    
    return {
      totalAppointments: appointments.data?.length || 0,
      totalUsers: users.data?.length || 0,
      totalBranches: branches.data?.length || 0,
      revenue: 12500, // This would come from your revenue API
    }
  })

  const statCards = [
    {
      title: 'Total Appointments',
      value: stats?.totalAppointments || 0,
      icon: Calendar,
      color: 'blue',
    },
    {
      title: 'Total Users',
      value: stats?.totalUsers || 0,
      icon: Users,
      color: 'green',
    },
    {
      title: 'Total Branches',
      value: stats?.totalBranches || 0,
      icon: Building,
      color: 'purple',
    },
    {
      title: 'Total Revenue',
      value: `$${stats?.revenue?.toLocaleString() || 0}`,
      icon: DollarSign,
      color: 'orange',
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <TrendingUp size={16} />
          <span>Last updated: {new Date().toLocaleTimeString()}</span>
        </div>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-2xl font-bold text-gray-800">{card.value}</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-full">
                <card.icon size={20} className="text-blue-500" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity and Charts would go here */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recent Activity
          </h2>
          {/* Activity list would go here */}
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Appointments Overview
          </h2>
          {/* Chart would go here */}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard