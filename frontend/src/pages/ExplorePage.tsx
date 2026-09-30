import axios from 'axios'
import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { ArrowLeft, LoaderCircle, MapPin, Search, SlidersHorizontal } from 'lucide-react'
import { getNearbyAmenities } from '../services/amenityService'
import { searchLocations } from '../services/locationService'
import type { AmenityCategory, NearbyAmenity } from '../types/amenity'
import type { LocationSearchResult } from '../types/location'
import { UrbanEaseMap } from '../components/map/UrbanEaseMap'

const radiusOptions = [
  { value: 500, label: '500 m' },
  { value: 1000, label: '1 km' },
  { value: 2000, label: '2 km' },
  { value: 5000, label: '5 km' },
] as const

const categoryOptions: { value: AmenityCategory | 'all'; label: string }[] = [
  { value: 'all', label: 'All places' },
  { value: 'grocery', label: 'Grocery' },
  { value: 'hospital', label: 'Hospitals' },
  { value: 'pharmacy', label: 'Pharmacies' },
  { value: 'bank', label: 'Banks' },
  { value: 'restaurant', label: 'Restaurants' },
  { value: 'bus_stop', label: 'Transport' },
  { value: 'school', label: 'Schools' },
]

function locationFromSearchParams(searchParams: URLSearchParams): LocationSearchResult | null {
  const latitude = Number(searchParams.get('lat'))
  const longitude = Number(searchParams.get('lng'))
  const name = searchParams.get('name')
  const displayName = searchParams.get('display')
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude) || !name || !displayName) {
    return null
  }
  return { id: null, name, display_name: displayName, latitude, longitude, address: {} }
}

function formatCategory(category: AmenityCategory): string {
  return category.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function ExplorePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [query, setQuery] = useState(searchParams.get('query') ?? '')
  const [selectedLocation, setSelectedLocation] = useState<LocationSearchResult | null>(() => locationFromSearchParams(searchParams))
  const [locationResults, setLocationResults] = useState<LocationSearchResult[]>([])
  const [locationLoading, setLocationLoading] = useState(false)
  const [locationError, setLocationError] = useState<string | null>(null)
  const [radius, setRadius] = useState(1000)
  const [category, setCategory] = useState<AmenityCategory | 'all'>('all')
  const [amenities, setAmenities] = useState<NearbyAmenity[]>([])
  const [amenityLoading, setAmenityLoading] = useState(false)
  const [amenityError, setAmenityError] = useState<string | null>(null)
  const [selectedAmenity, setSelectedAmenity] = useState<NearbyAmenity | null>(null)
  const searchAbortRef = useRef<AbortController | null>(null)

  useEffect(() => () => searchAbortRef.current?.abort(), [])

  useEffect(() => {
    if (!selectedLocation) {
      return
    }

    const controller = new AbortController()
    setAmenityLoading(true)
    setAmenityError(null)
    setSelectedAmenity(null)

    getNearbyAmenities(selectedLocation.latitude, selectedLocation.longitude, radius, undefined, controller.signal)
      .then((response) => setAmenities(response.amenities))
      .catch((error: unknown) => {
        if (!axios.isCancel(error)) {
          setAmenityError('We could not load nearby places. Try again.')
          setAmenities([])
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setAmenityLoading(false)
        }
      })

    return () => controller.abort()
  }, [radius, selectedLocation])

  const visibleAmenities = useMemo(
    () => (category === 'all' ? amenities : amenities.filter((amenity) => amenity.category === category)),
    [amenities, category],
  )

  async function handleLocationSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const normalizedQuery = query.trim()
    if (normalizedQuery.length < 2) {
      setLocationError('Enter at least 2 characters to search.')
      setLocationResults([])
      return
    }

    searchAbortRef.current?.abort()
    const controller = new AbortController()
    searchAbortRef.current = controller
    setLocationLoading(true)
    setLocationError(null)
    try {
      const results = await searchLocations(normalizedQuery, 5, controller.signal)
      if (!controller.signal.aborted) {
        setLocationResults(results)
        if (results.length === 0) {
          setLocationError('No matching places found.')
        }
      }
    } catch (error: unknown) {
      if (!axios.isCancel(error)) {
        setLocationResults([])
        setLocationError('Location search is unavailable right now.')
      }
    } finally {
      if (!controller.signal.aborted) {
        setLocationLoading(false)
      }
    }
  }

  function selectLocation(location: LocationSearchResult) {
    setSelectedLocation(location)
    setQuery(location.name)
    setLocationResults([])
    setLocationError(null)
    setSearchParams({
      query: location.name,
      lat: String(location.latitude),
      lng: String(location.longitude),
      name: location.name,
      display: location.display_name,
    })
  }

  function retryAmenities() {
    if (selectedLocation) {
      setSelectedLocation({ ...selectedLocation })
    }
  }

  const resultCount = visibleAmenities.length

  return (
    <main className="mx-auto max-w-[1500px] px-4 pb-16 pt-8 sm:px-6 lg:px-8">
      <div className="mb-7 flex items-center justify-between gap-4">
        <div>
          <Link to="/" className="mb-4 inline-flex items-center gap-2 text-sm font-medium text-slate-500 transition hover:text-slate-900">
            <ArrowLeft className="h-4 w-4" />
            Back home
          </Link>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700">Explore a place</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Find what is close by.</h1>
          <p className="mt-2 max-w-2xl text-slate-600">Search a neighborhood, then inspect essential places around it.</p>
        </div>
        <div className="hidden items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-800 sm:flex">
          <MapPin className="h-4 w-4" />
          OpenStreetMap data
        </div>
      </div>

      <section className="overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-sm shadow-slate-200/50">
        <div className="border-b border-slate-200 p-4 sm:p-5">
          <form className="flex flex-col gap-3 lg:flex-row" onSubmit={handleLocationSearch}>
            <label className="sr-only" htmlFor="location-search">Search for a city, neighborhood, or landmark</label>
            <div className="flex min-w-0 flex-1 items-center gap-3 rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 focus-within:border-slate-900 focus-within:ring-2 focus-within:ring-slate-900/10">
              <Search className="h-5 w-5 shrink-0 text-slate-400" />
              <input
                id="location-search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search Hadapsar, Pune"
                className="min-w-0 flex-1 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400"
              />
            </div>
            <button
              type="submit"
              disabled={locationLoading}
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-slate-950 px-6 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-wait disabled:opacity-70"
            >
              {locationLoading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
              Search
            </button>
          </form>
          {locationError && <p className="mt-3 text-sm text-rose-700" role="status">{locationError}</p>}
          {locationResults.length > 0 && (
            <div className="mt-3 divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white" role="listbox" aria-label="Location results">
              {locationResults.map((location) => (
                <button
                  key={`${location.id ?? location.display_name}-${location.latitude}`}
                  type="button"
                  className="flex w-full items-start gap-3 px-4 py-3 text-left transition hover:bg-slate-50"
                  onClick={() => selectLocation(location)}
                >
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-emerald-700" />
                  <span className="min-w-0">
                    <span className="block font-semibold text-slate-900">{location.name}</span>
                    <span className="block truncate text-sm text-slate-500">{location.display_name}</span>
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_300px]">
          <div className="order-2 min-w-0 lg:order-1">
            <UrbanEaseMap selectedLocation={selectedLocation} amenities={visibleAmenities} onSelectAmenity={setSelectedAmenity} />
          </div>
          <aside className="order-1 border-b border-slate-200 bg-slate-50/70 p-4 lg:order-2 lg:border-b-0 lg:border-l sm:p-5">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-900">
              <SlidersHorizontal className="h-4 w-4 text-slate-500" />
              Nearby places
            </div>

            <fieldset className="mt-5">
              <legend className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Radius</legend>
              <div className="mt-2 grid grid-cols-4 gap-2 lg:grid-cols-2">
                {radiusOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    aria-pressed={radius === option.value}
                    className={`min-h-10 rounded-lg border px-2 text-sm font-medium transition ${
                      radius === option.value
                        ? 'border-slate-950 bg-slate-950 text-white'
                        : 'border-slate-200 bg-white text-slate-600 hover:border-slate-400'
                    }`}
                    onClick={() => setRadius(option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </fieldset>

            <fieldset className="mt-6">
              <legend className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Category</legend>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {categoryOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    aria-pressed={category === option.value}
                    className={`min-h-10 rounded-lg border px-2 text-left text-xs font-medium transition ${
                      category === option.value
                        ? 'border-emerald-700 bg-emerald-700 text-white'
                        : 'border-slate-200 bg-white text-slate-600 hover:border-slate-400'
                    }`}
                    onClick={() => setCategory(option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </fieldset>

            <div className="mt-7 border-t border-slate-200 pt-5">
              {selectedLocation ? (
                <>
                  <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Showing around</p>
                  <p className="mt-2 font-semibold text-slate-900">{selectedLocation.name}</p>
                  <p className="mt-1 text-xs leading-5 text-slate-500">{selectedLocation.display_name}</p>
                </>
              ) : (
                <p className="text-sm leading-6 text-slate-600">Search for a place to load nearby amenities on the map.</p>
              )}
            </div>
          </aside>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 px-4 py-4 sm:px-5">
          <div className="flex items-center gap-3 text-sm text-slate-600" role="status" aria-live="polite">
            {amenityLoading && <LoaderCircle className="h-4 w-4 animate-spin text-emerald-700" />}
            {amenityLoading && 'Loading nearby places...'}
            {!amenityLoading && amenityError && <span className="text-rose-700">{amenityError}</span>}
            {!amenityLoading && !amenityError && selectedLocation && resultCount === 0 && `No amenities found within ${radius >= 1000 ? `${radius / 1000} km` : `${radius} m`}.`}
            {!amenityLoading && !amenityError && selectedLocation && resultCount > 0 && `${resultCount} place${resultCount === 1 ? '' : 's'} shown within ${radius >= 1000 ? `${radius / 1000} km` : `${radius} m`}.`}
          </div>
          {amenityError && (
            <button type="button" onClick={retryAmenities} className="text-sm font-semibold text-slate-900 underline underline-offset-4">
              Try again
            </button>
          )}
          {selectedAmenity && !amenityError && (
            <span className="text-xs text-slate-500">Selected: {selectedAmenity.name ?? formatCategory(selectedAmenity.category)}</span>
          )}
        </div>
      </section>
    </main>
  )
}