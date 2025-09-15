import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

// Context Providers
import { AuthProvider } from './contexts/AuthContext'
import { AppProvider } from './contexts/AppContext'

// Components
import ProtectedRoute from './components/auth/ProtectedRoute'
import Layout from './components/common/Layout/Layout'

// Pages
import Login from './pages/Login'
import AdminDashboard from './pages/Admin/Dashboard'
import EmployeeDashboard from './pages/Employee/Dashboard'
import DoctorDashboard from './pages/Doctor/Dashboard'

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
        <AppProvider>
          <Router>
            <div className="App">
              <Routes>
                <Route path="/login" element={<Login />} />
                
                {/* Admin Routes */}
                <Route path="/admin/*" element={
                  <ProtectedRoute allowedRoles={['ADMIN']}>
                    <Layout>
                      <Routes>
                        <Route path="dashboard" element={<AdminDashboard />} />
                        <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
                      </Routes>
                    </Layout>
                  </ProtectedRoute>
                } />
                
                {/* Employee Routes */}
                <Route path="/employee/*" element={
                  <ProtectedRoute allowedRoles={['EMPLOYEE']}>
                    <Layout>
                      <Routes>
                        <Route path="dashboard" element={<EmployeeDashboard />} />
                        <Route path="*" element={<Navigate to="/employee/dashboard" replace />} />
                      </Routes>
                    </Layout>
                  </ProtectedRoute>
                } />
                
                {/* Doctor Routes */}
                <Route path="/doctor/*" element={
                  <ProtectedRoute allowedRoles={['DOCTOR']}>
                    <Layout>
                      <Routes>
                        <Route path="dashboard" element={<DoctorDashboard />} />
                        <Route path="*" element={<Navigate to="/doctor/dashboard" replace />} />
                      </Routes>
                    </Layout>
                  </ProtectedRoute>
                } />
                
                {/* Default Route */}
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
              </Routes>
              
              <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
              />
            </div>
          </Router>
        </AppProvider>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App