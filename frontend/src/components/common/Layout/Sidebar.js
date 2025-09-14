import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Building, 
  UserCog, 
  Calendar,
  FileText,
  BarChart3,
  Settings
} from 'lucide-react'
import { useAuth } from '../../../hooks/useAuth'

const Sidebar = () => {
  const { user } = useAuth()

  const adminMenu = [
    { path: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/users', label: 'User Management', icon: Users },
    { path: '/admin/branches', label: 'Branches', icon: Building },
    { path: '/admin/doctors', label: 'Doctors', icon: UserCog },
    { path: '/admin/appointments', label: 'Appointments', icon: Calendar },
    { path: '/admin/reports', label: 'Reports', icon: BarChart3 },
    { path: '/admin/settings', label: 'Settings', icon: Settings },
  ]

  const employeeMenu = [
    { path: '/employee/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/employee/appointments', label: 'Appointments', icon: Calendar },
    { path: '/employee/patients', label: 'Patients', icon: Users },
    { path: '/employee/prescriptions', label: 'Prescriptions', icon: FileText },
  ]

  const doctorMenu = [
    { path: '/doctor/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/doctor/appointments', label: 'My Appointments', icon: Calendar },
    { path: '/doctor/prescriptions', label: 'Prescriptions', icon: FileText },
    { path: '/doctor/patients', label: 'Patients', icon: Users },
  ]

  const getMenu = () => {
    switch (user?.role) {
      case 'ADMIN': return adminMenu
      case 'EMPLOYEE': return employeeMenu
      case 'DOCTOR': return doctorMenu
      default: return []
    }
  }

  return (
    <aside className="w-64 bg-white shadow-lg">
      <div className="p-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
            <LayoutDashboard size={20} className="text-white" />
          </div>
          <span className="text-xl font-semibold text-gray-800">DAS</span>
        </div>
      </div>
      
      <nav className="mt-6">
        {getMenu().map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-6 py-3 text-gray-600 hover:bg-blue-50 hover:text-blue-600 ${
                isActive ? 'bg-blue-50 text-blue-600 border-r-2 border-blue-600' : ''
              }`
            }
          >
            <item.icon size={18} className="mr-3" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar