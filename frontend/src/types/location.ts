export type LocationAddress = Record<string, string>

export interface LocationSearchResult {
  id: string | null
  name: string
  display_name: string
  latitude: number
  longitude: number
  address: LocationAddress
}