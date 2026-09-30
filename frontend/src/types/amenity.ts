export type AmenityCategory =
  | 'grocery'
  | 'hospital'
  | 'pharmacy'
  | 'bank'
  | 'atm'
  | 'bus_stop'
  | 'metro_station'
  | 'restaurant'
  | 'hotel'
  | 'petrol_pump'
  | 'police_station'
  | 'laundry'
  | 'gym'
  | 'school'
  | 'college'

export interface NearbyAmenity {
  id: string
  osm_id: string | null
  osm_type: string | null
  name: string | null
  category: AmenityCategory
  latitude: number
  longitude: number
  distance_meters: number
  address: string | null
  opening_hours: string | null
  phone: string | null
  website: string | null
}

export interface NearbyAmenitiesResponse {
  center: { latitude: number; longitude: number }
  radius_meters: number
  category: AmenityCategory | null
  count: number
  amenities: NearbyAmenity[]
}