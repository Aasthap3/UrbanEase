import L from 'leaflet'
import type { AmenityCategory } from '../../types/amenity'

const categorySymbols: Record<AmenityCategory, string> = {
  grocery: 'G',
  hospital: 'H',
  pharmacy: 'P',
  bank: 'B',
  atm: 'A',
  bus_stop: 'B',
  metro_station: 'M',
  restaurant: 'R',
  hotel: 'H',
  petrol_pump: 'F',
  police_station: 'S',
  laundry: 'L',
  gym: 'Y',
  school: 'C',
  college: 'C',
}

const categoryColors: Record<AmenityCategory, string> = {
  grocery: '#0f766e',
  hospital: '#dc2626',
  pharmacy: '#2563eb',
  bank: '#7c3aed',
  atm: '#6d28d9',
  bus_stop: '#b45309',
  metro_station: '#c2410c',
  restaurant: '#ea580c',
  hotel: '#be123c',
  petrol_pump: '#475569',
  police_station: '#1d4ed8',
  laundry: '#0891b2',
  gym: '#15803d',
  school: '#a16207',
  college: '#9333ea',
}

function createMarkerIcon(className: string, symbol: string, color: string): L.DivIcon {
  return L.divIcon({
    className: 'urbanease-marker-wrapper',
    html: `<span class="urbanease-marker ${className}" style="--marker-color:${color}" aria-hidden="true"><span class="urbanease-marker-glyph">${symbol}</span></span>`,
    iconSize: [34, 42],
    iconAnchor: [17, 38],
    popupAnchor: [0, -38],
  })
}

export function getAmenityIcon(category: AmenityCategory): L.DivIcon {
  return createMarkerIcon('urbanease-amenity-marker', categorySymbols[category], categoryColors[category])
}

export const selectedLocationIcon = createMarkerIcon('urbanease-location-marker', '●', '#0f172a')