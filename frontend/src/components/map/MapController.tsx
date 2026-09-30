import { useEffect } from 'react'
import { useMap } from 'react-leaflet'

interface MapControllerProps {
  latitude: number
  longitude: number
}

export function MapController({ latitude, longitude }: MapControllerProps) {
  const map = useMap()

  useEffect(() => {
    map.flyTo([latitude, longitude], Math.max(map.getZoom(), 13), { duration: 0.8 })
  }, [latitude, longitude, map])

  return null
}