import type { PreferenceResponse, PreferenceUpdate } from '../types/preferences'
import { apiClient } from './apiClient'

export async function getPreferences(): Promise<PreferenceResponse> {
  const response = await apiClient.get<PreferenceResponse>('/api/preferences')
  return response.data
}

export async function updatePreferences(profile: PreferenceUpdate['profile'], weights: PreferenceUpdate['weights']): Promise<PreferenceResponse> {
  const response = await apiClient.put<PreferenceResponse>('/api/preferences', { profile, weights })
  return response.data
}