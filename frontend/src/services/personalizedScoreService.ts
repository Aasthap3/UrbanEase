import type { PersonalizedScoreResponse } from '../types/urbanScore'
import { apiClient } from './apiClient'

export async function getPersonalizedScore(
  latitude: number,
  longitude: number,
  radius: number,
  signal?: AbortSignal,
): Promise<PersonalizedScoreResponse> {
  const response = await apiClient.get<PersonalizedScoreResponse>('/api/score/personalized', {
    params: { latitude, longitude, radius },
    signal,
  })
  return response.data
}