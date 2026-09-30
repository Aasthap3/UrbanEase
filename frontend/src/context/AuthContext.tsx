import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import axios from 'axios'
import { getCurrentUser, login as loginRequest, register as registerRequest } from '../services/authService'
import type { LoginRequest, RegisterRequest, User } from '../types/auth'

interface AuthContextValue {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (request: LoginRequest) => Promise<void>
  register: (request: RegisterRequest) => Promise<User>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  function clearSession() {
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
  }

  async function refreshUser() {
    const storedToken = localStorage.getItem('access_token')
    if (!storedToken) {
      setToken(null)
      setUser(null)
      return
    }
    try {
      const currentUser = await getCurrentUser()
      setToken(storedToken)
      setUser(currentUser)
    } catch {
      clearSession()
    }
  }

  useEffect(() => {
    let active = true
    refreshUser().finally(() => {
      if (active) {
        setIsLoading(false)
      }
    })
    const handleAuthExpired = () => clearSession()
    window.addEventListener('urbanease:auth-expired', handleAuthExpired)
    return () => {
      active = false
      window.removeEventListener('urbanease:auth-expired', handleAuthExpired)
    }
  }, [])

  async function login(request: LoginRequest) {
    const response = await loginRequest(request)
    localStorage.setItem('access_token', response.access_token)
    setToken(response.access_token)
    await refreshUser()
  }

  async function register(request: RegisterRequest) {
    return registerRequest(request)
  }

  const value = useMemo<AuthContextValue>(() => ({
    user,
    token,
    isAuthenticated: Boolean(user && token),
    isLoading,
    login,
    register,
    logout: clearSession,
    refreshUser,
  }), [isLoading, token, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}

export function getAuthErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error) && error.response?.status === 401) {
    return 'Invalid email or password.'
  }
  if (axios.isAxiosError(error) && error.response?.status === 409) {
    return 'An account with this email already exists.'
  }
  return fallback
}