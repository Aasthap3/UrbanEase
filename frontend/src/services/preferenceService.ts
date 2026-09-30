import axios from 'axios'
import type { PreferenceResponse, PreferenceUpdate } from '../types/preferences'

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function authConfig() {
  const token = localStorage.getItem('access_token')
  return token ? { headers: { Authorization: `Bearer ${token}` } } : undefined
}

export function hasStoredAuthentication(): boolean {
  return Boolean(localStorage.getItem('access_token'))
}

export async function getPreferences(): Promise<PreferenceResponse> {
  const response = await axios.get<PreferenceResponse>(`${apiUrl}/api/preferences`, authConfig())
  return response.data
}

export async function updatePreferences(profile: PreferenceUpdate['profile'], weights: PreferenceUpdate['weights']): Promise<PreferenceResponse> {
  const response = await axios.put<PreferenceResponse>(`${apiUrl}/api/preferences`, { profile, weights }, authConfig())
  return response.data
}