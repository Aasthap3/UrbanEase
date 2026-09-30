import axios from 'axios'
import type { LocationSearchResult } from '../types/location'

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function searchLocations(query: string, limit = 5, signal?: AbortSignal): Promise<LocationSearchResult[]> {
  const response = await axios.get<LocationSearchResult[]>(`${apiUrl}/api/locations/search`, {
    params: { q: query, limit },
    signal,
  })
  return response.data
}