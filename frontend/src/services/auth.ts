import api from './api'

export interface AuthUser {
  id: string
  full_name: string
  email: string
  role: 'student' | 'admin'
}

interface AuthResponse {
  data: {
    access_token: string
    user: AuthUser
  }
}

interface RegisterPayload {
  full_name: string
  email: string
  password: string
}

interface LoginPayload {
  email: string
  password: string
}

export async function register(payload: RegisterPayload): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>('/auth/register', payload)
  return response.data
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>('/auth/login', payload)
  return response.data
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await api.get<{ data: AuthUser }>('/auth/me')
  return response.data.data
}