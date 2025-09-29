import React, { useState } from 'react'
import { Eye, EyeOff, LogIn } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { useNotification } from '../hooks/useNotification'

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '', 
    password: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  
  //const { login } = useAuth()
  const { showError } = useNotification()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const result = await login(credentials)
      if (!result.success) {
        showError(result.error)
      }
    } catch (error) {
      showError('Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-lg shadow-lg transform transition duration-300 ease-in-out hover:scale-105">
        <div className="flex justify-center">
          <div className="w-16 h-16 bg-blue-500 rounded-lg flex items-center justify-center shadow-xl">
            <LogIn size={32} className="text-white animate-pulse" />
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 animate__animated animate__fadeIn">Doctor Appointment System</h2>
        <p className="mt-2 text-center text-sm text-gray-600">Sign in to your account</p>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="username" className="sr-only">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-transparent text-gray-900 rounded-t-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm transition-all duration-300"
                placeholder="Username"
                value={credentials.username}
                onChange={handleChange}
              />
              <span className="absolute left-3 top-2 text-gray-500 text-sm transition-all duration-300">{credentials.username ? '' : 'Username'}</span>
            </div>
            <div className="relative mt-6">
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-transparent text-gray-900 rounded-b-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm transition-all duration-300"
                placeholder="Password"
                value={credentials.password}
                onChange={handleChange}
              />
              <span className="absolute left-3 top-2 text-gray-500 text-sm transition-all duration-300">{credentials.password ? '' : 'Password'}</span>
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={16} className="text-gray-400" /> : <Eye size={16} className="text-gray-400" />}
              </button>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login;
