import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

// Context Providers
import { AuthProvider } from './contexts/AuthContext'
import { AppProvider } from './contexts/AppContext'

// Components
import ProtectedRoute from './components/auth/ProtectedRoute'
import Layout from './components/common/Layout/Layout'

// Pages
import Login from './pages/Login.jsx'
import AdminDashboard from './pages/Admin/Dashboard'
import EmployeeDashboard from './pages/Employee/Dashboard'
import DoctorDashboard from './pages/Doctor/Dashboard'
import UserManagement from './pages/Admin/UserManagement'
import BranchManagement from './pages/Admin/BranchManagement'
import DoctorManagement from './pages/Admin/DoctorManagement'
import AppointmentManagement from './pages/Employee/AppointmentManagement'
import PatientSearch from './pages/Employee/PatientSearch'
import DoctorAppointments from './pages/Doctor/Appointments'
import DoctorPrescriptions from './pages/Doctor/Prescriptions'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
          <Router>
            <div className="App">
              <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />

                {/* Admin */}
                <Route
                  path="/admin/*"
                  element={
                    <ProtectedRoute allowedRoles={['ADMIN']}>
                      <Layout />
                    </ProtectedRoute>
                  }
                >
                  <Route path="dashboard" element={<AdminDashboard />} />
                  <Route path="users" element={<UserManagement />} />
                  <Route path="branches" element={<BranchManagement />} />
                  <Route path="doctors" element={<DoctorManagement />} />
                  <Route path="*" element={<Navigate to="dashboard" replace />} />
                </Route>

                {/* Employee */}
                <Route
                  path="/employee/*"
                  element={
                    <ProtectedRoute allowedRoles={['EMPLOYEE']}>
                      <Layout />
                    </ProtectedRoute>
                  }
                >
                  <Route path="dashboard" element={<EmployeeDashboard />} />
                  <Route path="appointments" element={<AppointmentManagement />} />
                  <Route path="patients" element={<PatientSearch />} />
                  <Route path="*" element={<Navigate to="dashboard" replace />} />
                </Route>

                {/* Doctor */}
                <Route
                  path="/doctor/*"
                  element={
                    <ProtectedRoute allowedRoles={['DOCTOR']}>
                      <Layout />
                    </ProtectedRoute>
                  }
                >
                  <Route path="dashboard" element={<DoctorDashboard />} />
                  <Route path="appointments" element={<DoctorAppointments />} />
                  <Route path="prescriptions" element={<DoctorPrescriptions />} />
                  <Route path="*" element={<Navigate to="dashboard" replace />} />
                </Route>

                {/* Default */}
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
              </Routes>

              <ToastContainer position="top-right" autoClose={5000} />
            </div>
          </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
