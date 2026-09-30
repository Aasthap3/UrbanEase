import { Marker, Popup } from 'react-leaflet'
import type { NearbyAmenity } from '../../types/amenity'
import { getAmenityIcon } from './amenityIcons'

interface AmenityMarkerProps {
  amenity: NearbyAmenity
  onSelect?: (amenity: NearbyAmenity) => void
}

function formatCategory(category: string): string {
  return category.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function AmenityMarker({ amenity, onSelect }: AmenityMarkerProps) {
  return (
    <Marker
      position={[amenity.latitude, amenity.longitude]}
      icon={getAmenityIcon(amenity.category)}
      eventHandlers={{ click: () => onSelect?.(amenity) }}
    >
      <Popup>
        <div className="min-w-44 space-y-2 text-slate-900">
          <div>
            <p className="font-semibold">{amenity.name ?? 'Unnamed place'}</p>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{formatCategory(amenity.category)}</p>
          </div>
          <p className="text-sm font-medium text-emerald-700">{Math.round(amenity.distance_meters)} m away</p>
          {amenity.address && <p className="text-xs text-slate-600">{amenity.address}</p>}
          {amenity.opening_hours && <p className="text-xs text-slate-600">Hours: {amenity.opening_hours}</p>}
          {amenity.phone && (
            <a className="block text-xs text-blue-700 underline" href={`tel:${amenity.phone}`}>
              {amenity.phone}
            </a>
          )}
          {amenity.website && (
            <a
              className="block text-xs text-blue-700 underline"
              href={amenity.website}
              target="_blank"
              rel="noreferrer"
            >
              Visit website
            </a>
          )}
        </div>
      </Popup>
    </Marker>
  )
}