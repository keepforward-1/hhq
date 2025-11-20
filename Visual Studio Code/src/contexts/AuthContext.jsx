import React, { createContext, useState, useContext, useEffect } from 'react'
import axios from 'axios'
import { message } from 'antd'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth必须在AuthProvider内使用')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        const response = await axios.get('/api/auth/me')
        setUser(response.data.user)
        setIsAuthenticated(true)
      } catch (error) {
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    }
    setLoading(false)
  }

  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/auth/login', {
        username,
        password
      })
      const { access_token, user } = response.data
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setUser(user)
      setIsAuthenticated(true)
      message.success('登录成功')
      return true
    } catch (error) {
      message.error(error.response?.data?.error || '登录失败')
      return false
    }
  }

  const register = async (username, email, password, nickname) => {
    try {
      const response = await axios.post('/api/auth/register', {
        username,
        email,
        password,
        nickname
      })
      message.success('注册成功，请登录')
      return true
    } catch (error) {
      message.error(error.response?.data?.error || '注册失败')
      return false
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
    setIsAuthenticated(false)
    message.success('已退出登录')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

