import React from 'react'
import { Users, Plus } from 'lucide-react'
import { useQuery } from "@tanstack/react-query";
import { usersAPI } from '../../services'

const UserManagement = () => {
  const { data: users, isLoading, error } = useQuery('users', usersAPI.list)

  if (isLoading) return <div>Loading users...</div>
  if (error) return <div>Error loading users: {error.message}</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center">
          <Users className="mr-2" size={24} />
          User Management
        </h1>
        <button className="btn-primary flex items-center">
          <Plus size={16} className="mr-1" />
          Add User
        </button>
      </div>

      <div className="card p-6">
        <div className="table-container">
          <table className="table">
            <thead className="table-head">
              <tr>
                <th className="table-header">Username</th>
                <th className="table-header">Email</th>
                <th className="table-header">Role</th>
                <th className="table-header">Branch</th>
                <th className="table-header">Status</th>
                <th className="table-header">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users?.data?.map((user) => (
                <tr key={user.id} className="table-row">
                  <td className="table-cell">{user.username}</td>
                  <td className="table-cell">{user.email}</td>
                  <td className="table-cell capitalize">{user.role?.toLowerCase()}</td>
                  <td className="table-cell">{user.branch_name || 'N/A'}</td>
                  <td className="table-cell">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="table-cell">
                    <div className="flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-800 text-sm">
                        Edit
                      </button>
                      <button className="text-red-600 hover:text-red-800 text-sm">
                        Delete
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

export default UserManagement