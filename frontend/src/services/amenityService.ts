import axios from 'axios'
import type { AmenityCategory, NearbyAmenitiesResponse } from '../types/amenity'

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function getNearbyAmenities(
  latitude: number,
  longitude: number,
  radius: number,
  category?: AmenityCategory,
  signal?: AbortSignal,
): Promise<NearbyAmenitiesResponse> {
  const response = await axios.get<NearbyAmenitiesResponse>(`${apiUrl}/api/amenities/nearby`, {
    params: { latitude, longitude, radius, category },
    signal,
  })
  return response.data
}