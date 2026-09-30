import axios from 'axios'
import type { PersonalizedScoreResponse } from '../types/urbanScore'

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function getPersonalizedScore(
  latitude: number,
  longitude: number,
  radius: number,
  signal?: AbortSignal,
): Promise<PersonalizedScoreResponse> {
  const token = localStorage.getItem('access_token')
  const response = await axios.get<PersonalizedScoreResponse>(`${apiUrl}/api/score/personalized`, {
    params: { latitude, longitude, radius },
    signal,
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  })
  return response.data
}