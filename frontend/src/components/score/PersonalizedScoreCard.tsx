import { LoaderCircle, RefreshCw, Sparkles } from 'lucide-react'
import type { AmenityCategory } from '../../types/amenity'
import type { PersonalizedScoreResponse } from '../../types/urbanScore'

interface PersonalizedScoreCardProps {
  score: PersonalizedScoreResponse | null
  loading: boolean
  error: string | null
  onRetry: () => void
}

function formatCategory(category: AmenityCategory): string {
  return category.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function PersonalizedScoreCard({ score, loading, error, onRetry }: PersonalizedScoreCardProps) {
  return (
    <section className="mt-6 rounded-[24px] border border-emerald-200 bg-emerald-50/50 p-5 sm:p-6" aria-labelledby="personalized-score-heading">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700"><Sparkles className="h-4 w-4" /> Your score</div>
          <h2 id="personalized-score-heading" className="mt-2 text-2xl font-semibold tracking-tight text-slate-950">Personalized UrbanEase Score</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">Your score reflects nearby accessibility according to your selected priorities. Closer amenities contribute more strongly.</p>
        </div>
        <div className="shrink-0 text-right">
          <span className="block text-3xl font-semibold text-slate-950">{loading ? '—' : score?.score.toFixed(1) ?? '—'}</span>
          <span className="text-xs text-slate-500">/ 100</span>
        </div>
      </div>
      {loading && <div className="mt-5 flex items-center gap-2 text-sm text-slate-600" role="status"><LoaderCircle className="h-4 w-4 animate-spin text-emerald-700" />Calculating personalized score...</div>}
      {error && <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800" role="alert"><span>{error}</span><button type="button" onClick={onRetry} className="inline-flex items-center gap-2 font-semibold underline underline-offset-4"><RefreshCw className="h-3.5 w-3.5" />Try again</button></div>}
      {!loading && !error && score && <>
        <div className="mt-4 flex flex-wrap gap-2 text-xs font-medium text-slate-600"><span className="rounded-full bg-white px-3 py-1">Profile: {score.profile.replace('_', ' ')}</span><span className="rounded-full bg-white px-3 py-1">Weights: {score.weight_total.toFixed(1)} / 100</span></div>
        <div className="mt-5 grid gap-x-8 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
          {score.categories.map((category) => <div key={category.category}><div className="mb-1 flex justify-between gap-2 text-sm"><span className="font-medium text-slate-800">{formatCategory(category.category)}</span><span className="text-slate-500">{Math.round(category.score * 100)}%</span></div><div className="h-2 overflow-hidden rounded-full bg-white"><div className="h-full rounded-full bg-emerald-600" style={{ width: `${category.score * 100}%` }} /></div><div className="mt-1 flex justify-between text-[11px] text-slate-500"><span>{category.contribution.toFixed(1)} contribution</span><span>weight {category.weight}</span></div></div>)}
        </div>
      </>}
    </section>
  )
}