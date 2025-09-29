import React from 'react'
import { 
  Users, 
  Building, 
  Calendar, 
  DollarSign,
  TrendingUp,
  ArrowUp
} from 'lucide-react'
import { useQuery } from "@tanstack/react-query"
import { appointmentsAPI, usersAPI, branchesAPI } from '../../services'

const AdminDashboard = () => {
  // Fetch stats from APIs
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
      revenue: 12500, // Example: could come from revenue API
    }
  })

  // Stat cards with changes
  const statCards = [
    { 
      label: 'Total Patients', 
      value: stats?.totalUsers?.toLocaleString() || '0', 
      change: '+12%', 
      icon: Users, 
      color: 'blue' 
    },
    { 
      label: 'Total Appointments', 
      value: stats?.totalAppointments?.toLocaleString() || '0', 
      change: '+8%', 
      icon: Calendar, 
      color: 'green' 
    },
    { 
      label: 'Total Revenue', 
      value: `$${stats?.revenue?.toLocaleString() || '0'}`, 
      change: '+15%', 
      icon: DollarSign, 
      color: 'purple' 
    },
    { 
      label: 'Branches', 
      value: stats?.totalBranches?.toLocaleString() || '0', 
      change: '+0%', 
      icon: Building, 
      color: 'orange' 
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <TrendingUp size={16} />
          <span>Last updated: {new Date().toLocaleTimeString()}</span>
        </div>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                <div className="flex items-center mt-1">
                  <ArrowUp size={14} className="text-green-500" />
                  <span className="text-sm text-green-500 ml-1">{stat.change}</span>
                  <span className="text-sm text-gray-500 ml-2">from last week</span>
                </div>
              </div>
              <div className={`p-3 rounded-full bg-${stat.color}-100`}>
                <stat.icon size={20} className={`text-${stat.color}-500`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity + Quick Actions / Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {[1, 2, 3].map((item) => (
              <div key={item} className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Users size={16} className="text-blue-500" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">New patient registered</p>
                  <p className="text-xs text-gray-500">2 hours ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            <button className="btn-secondary">Manage Users</button>
            <button className="btn-secondary">View Reports</button>
            <button className="btn-secondary">Branch Settings</button>
            <button className="btn-secondary">System Config</button>
          </div>
        </div>
      </div>

      {/* Chart / Overview Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Appointments Overview</h2>
          {/* Chart goes here */}
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Revenue Overview</h2>
          {/* Revenue chart or insights here */}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
