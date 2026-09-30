import axios from 'axios'
import type { UrbanScoreResponse } from '../types/urbanScore'

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function getUrbanEaseScore(
  latitude: number,
  longitude: number,
  radius: number,
  signal?: AbortSignal,
): Promise<UrbanScoreResponse> {
  const response = await axios.get<UrbanScoreResponse>(`${apiUrl}/api/score`, {
    params: { latitude, longitude, radius },
    signal,
  })
  return response.data
}