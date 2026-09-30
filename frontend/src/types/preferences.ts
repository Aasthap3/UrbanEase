import type { AmenityCategory } from './amenity'

export type ProfileName = 'student' | 'working_professional' | 'family' | 'custom'

export interface PreferenceWeight {
  category: AmenityCategory
  weight: number
}

export interface PreferenceResponse {
  profile: ProfileName
  weights: PreferenceWeight[]
  weight_total: number
}

export interface PreferenceUpdate {
  profile: ProfileName
  weights: PreferenceWeight[]
}

export const scoringCategories: AmenityCategory[] = [
  'grocery',
  'hospital',
  'pharmacy',
  'bank',
  'atm',
  'bus_stop',
  'metro_station',
  'restaurant',
  'hotel',
  'petrol_pump',
  'police_station',
  'laundry',
  'gym',
  'school',
  'college',
]

export const profileLabels: Record<ProfileName, string> = {
  student: 'Student',
  working_professional: 'Working Professional',
  family: 'Family',
  custom: 'Custom',
}

const baselineWeights: Record<AmenityCategory, number> = {
  grocery: 12,
  hospital: 12,
  pharmacy: 10,
  bank: 6,
  atm: 5,
  bus_stop: 8,
  metro_station: 8,
  restaurant: 5,
  hotel: 2,
  petrol_pump: 5,
  police_station: 8,
  laundry: 3,
  gym: 3,
  school: 7,
  college: 6,
}

export const profileWeights: Record<ProfileName, Record<AmenityCategory, number>> = {
  student: {
    grocery: 12, hospital: 5, pharmacy: 10, bank: 3, atm: 2, bus_stop: 15, metro_station: 12,
    restaurant: 8, hotel: 1, petrol_pump: 1, police_station: 1, laundry: 1, gym: 1, school: 3, college: 25,
  },
  working_professional: {
    grocery: 15, hospital: 5, pharmacy: 10, bank: 10, atm: 8, bus_stop: 15, metro_station: 12,
    restaurant: 10, hotel: 3, petrol_pump: 3, police_station: 2, laundry: 2, gym: 2, school: 1, college: 2,
  },
  family: {
    grocery: 18, hospital: 18, pharmacy: 14, bank: 3, atm: 2, bus_stop: 10, metro_station: 4,
    restaurant: 3, hotel: 1, petrol_pump: 2, police_station: 8, laundry: 1, gym: 1, school: 14, college: 1,
  },
  custom: baselineWeights,
}

export function weightsForProfile(profile: ProfileName): PreferenceWeight[] {
  return scoringCategories.map((category) => ({ category, weight: profileWeights[profile][category] }))
}