import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types/auth'
import { apiClient } from './apiClient'

export async function login(request: LoginRequest): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>('/api/auth/login', request)
  return response.data
}

export async function register(request: RegisterRequest): Promise<User> {
  const response = await apiClient.post<User>('/api/auth/register', request)
  return response.data
}

export async function getCurrentUser(): Promise<User> {
  const response = await apiClient.get<User>('/api/auth/me')
  return response.data
}