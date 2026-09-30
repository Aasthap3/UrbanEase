import { LoaderCircle, RefreshCw, Sparkles } from 'lucide-react'
import type { AmenityCategory } from '../../types/amenity'
import type { UrbanScoreResponse } from '../../types/urbanScore'

interface UrbanEaseScoreCardProps {
  score: UrbanScoreResponse | null
  loading: boolean
  error: string | null
  onRetry: () => void
}

function formatCategory(category: AmenityCategory): string {
  return category.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function radiusLabel(radius: number): string {
  return radius >= 1000 ? `${radius / 1000} km` : `${radius} m`
}

export function UrbanEaseScoreCard({ score, loading, error, onRetry }: UrbanEaseScoreCardProps) {
  return (
    <section className="mt-6 rounded-[24px] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/50 sm:p-6" aria-labelledby="urban-ease-score-heading">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-xl">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">
            <Sparkles className="h-4 w-4" />
            Baseline accessibility metric
          </div>
          <h2 id="urban-ease-score-heading" className="mt-2 text-2xl font-semibold tracking-tight text-slate-950">UrbanEase Score</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Closer amenities contribute more strongly to this decision-support metric. It uses fixed baseline category weights and available OpenStreetMap data.
          </p>
        </div>
        <div className="min-w-40 rounded-2xl bg-slate-950 px-5 py-4 text-white">
          <p className="text-xs uppercase tracking-[0.14em] text-slate-400">{score ? `Within ${radiusLabel(score.radius_meters)}` : 'Select a location'}</p>
          <div className="mt-1 flex items-end gap-2">
            <span className="text-4xl font-semibold tracking-tight">{loading ? '—' : score?.score.toFixed(1) ?? '—'}</span>
            <span className="pb-1 text-sm text-slate-400">/ 100</span>
          </div>
        </div>
      </div>

      {loading && (
        <div className="mt-6 flex items-center gap-2 text-sm text-slate-600" role="status">
          <LoaderCircle className="h-4 w-4 animate-spin text-emerald-700" />
          Calculating accessibility score...
        </div>
      )}
      {error && (
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800" role="alert">
          <span>{error}</span>
          <button type="button" onClick={onRetry} className="inline-flex items-center gap-2 font-semibold underline underline-offset-4">
            <RefreshCw className="h-3.5 w-3.5" />
            Try again
          </button>
        </div>
      )}
      {!loading && !error && !score && (
        <p className="mt-6 rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-600">Search for a location to calculate its baseline accessibility score.</p>
      )}
      {!loading && !error && score && (
        <div className="mt-6 grid gap-x-8 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
          {score.categories.map((category) => (
            <div key={category.category}>
              <div className="mb-1 flex items-center justify-between gap-3 text-sm">
                <span className="font-medium text-slate-800">{formatCategory(category.category)}</span>
                <span className="text-slate-500">{Math.round(category.score * 100)}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-emerald-600 transition-[width]" style={{ width: `${category.score * 100}%` }} />
              </div>
              <div className="mt-1 flex justify-between gap-2 text-[11px] text-slate-500">
                <span>{category.amenity_count} found · weight {category.weight}</span>
                <span>{category.nearest_distance_meters === null ? 'No nearby match' : `${Math.round(category.nearest_distance_meters)} m`}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}