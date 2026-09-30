import type { NearbyAmenity } from '../../types/amenity'
import type { LocationSearchResult } from '../../types/location'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import { AmenityMarker } from './AmenityMarker'
import { MapController } from './MapController'
import { selectedLocationIcon } from './amenityIcons'

const defaultCenter: [number, number] = [18.5204, 73.8567]

interface UrbanEaseMapProps {
  selectedLocation: LocationSearchResult | null
  amenities: NearbyAmenity[]
  onSelectAmenity?: (amenity: NearbyAmenity) => void
}

export function UrbanEaseMap({ selectedLocation, amenities, onSelectAmenity }: UrbanEaseMapProps) {
  const center: [number, number] = selectedLocation
    ? [selectedLocation.latitude, selectedLocation.longitude]
    : defaultCenter

  return (
    <div className="urbanease-map-shell" aria-label="Nearby amenities map">
      <MapContainer center={center} zoom={selectedLocation ? 13 : 11} scrollWheelZoom className="urbanease-map">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {selectedLocation && (
          <>
            <MapController latitude={selectedLocation.latitude} longitude={selectedLocation.longitude} />
            <Marker position={[selectedLocation.latitude, selectedLocation.longitude]} icon={selectedLocationIcon}>
              <Popup>
                <div className="space-y-1 text-slate-900">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Selected location</p>
                  <p className="font-semibold">{selectedLocation.name}</p>
                  <p className="max-w-56 text-xs text-slate-600">{selectedLocation.display_name}</p>
                </div>
              </Popup>
            </Marker>
          </>
        )}
        {amenities.map((amenity) => (
          <AmenityMarker key={amenity.id} amenity={amenity} onSelect={onSelectAmenity} />
        ))}
      </MapContainer>
    </div>
  )
}