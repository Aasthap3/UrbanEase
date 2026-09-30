import type { AmenityCategory } from './amenity'

export interface CategoryScore {
  category: AmenityCategory
  weight: number
  score: number
  nearest_distance_meters: number | null
  amenity_count: number
  contribution: number
}

export interface UrbanScoreResponse {
  latitude: number
  longitude: number
  radius_meters: number
  score: number
  categories: CategoryScore[]
}

export interface PersonalizedScoreResponse extends UrbanScoreResponse {
  profile: string
  weight_total: number
}