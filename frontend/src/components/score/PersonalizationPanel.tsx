import { Check, LoaderCircle, LockKeyhole, Save } from 'lucide-react'
import type { AmenityCategory } from '../../types/amenity'
import type { PreferenceWeight, ProfileName } from '../../types/preferences'
import { profileLabels } from '../../types/preferences'

interface PersonalizationPanelProps {
  authenticated: boolean
  profile: ProfileName
  weights: PreferenceWeight[]
  error: string | null
  saving: boolean
  onProfileChange: (profile: ProfileName) => void
  onWeightChange: (category: AmenityCategory, weight: number) => void
  onApply: () => void
}

function formatCategory(category: AmenityCategory): string {
  return category.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
}

export function PersonalizationPanel({
  authenticated,
  profile,
  weights,
  error,
  saving,
  onProfileChange,
  onWeightChange,
  onApply,
}: PersonalizationPanelProps) {
  const total = weights.reduce((sum, item) => sum + item.weight, 0)
  const valid = Math.abs(total - 100) < 0.01

  return (
    <section className="mt-6 rounded-[24px] border border-slate-200 bg-white p-5 shadow-sm shadow-slate-200/50 sm:p-6" aria-labelledby="personalization-heading">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">Your priorities</p>
          <h2 id="personalization-heading" className="mt-2 text-2xl font-semibold tracking-tight text-slate-950">Personalize the score</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Profile weights are starting points. Adjust them to reflect your priorities; every category remains part of the explainable MCDA score.</p>
        </div>
        <div className="flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-2 text-xs font-medium text-slate-600">
          <LockKeyhole className="h-3.5 w-3.5" />
          Saved to your account
        </div>
      </div>

      {!authenticated ? (
        <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
          Sign in to personalize your UrbanEase Score. The public map and baseline score remain available.
        </div>
      ) : (
        <>
          <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <label className="block text-sm font-medium text-slate-700">
              Starting profile
              <select
                value={profile}
                onChange={(event) => onProfileChange(event.target.value as ProfileName)}
                className="mt-2 block min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3 text-sm text-slate-900 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10 sm:w-64"
              >
                {(Object.keys(profileLabels) as ProfileName[]).map((profileName) => (
                  <option key={profileName} value={profileName}>{profileLabels[profileName]}</option>
                ))}
              </select>
            </label>
            <div className={`text-sm font-semibold ${valid ? 'text-emerald-700' : 'text-rose-700'}`} role="status">
              {valid ? <Check className="mr-1 inline h-4 w-4" /> : null}
              Total Weight: {total.toFixed(1)} / 100{valid ? '' : ' · Weights must total 100%'}
            </div>
          </div>

          <div className="mt-5 grid gap-x-6 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
            {weights.map((item) => (
              <label key={item.category} className="text-sm text-slate-700">
                <span className="mb-1 flex items-center justify-between gap-2">
                  <span>{formatCategory(item.category)}</span>
                  <span className="text-xs text-slate-500">{item.weight}%</span>
                </span>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.1"
                  value={item.weight}
                  onChange={(event) => onWeightChange(item.category, Number(event.target.value))}
                  className="min-h-10 w-full rounded-lg border border-slate-300 bg-white px-3 text-sm outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10"
                  aria-label={`${formatCategory(item.category)} weight`}
                />
              </label>
            ))}
          </div>

          {error && <p className="mt-4 text-sm text-rose-700" role="alert">{error}</p>}
          <button
            type="button"
            disabled={!valid || saving}
            onClick={onApply}
            className="mt-5 inline-flex min-h-11 items-center gap-2 rounded-lg bg-emerald-700 px-4 text-sm font-semibold text-white transition hover:bg-emerald-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {saving ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
            Apply Preferences
          </button>
        </>
      )}
    </section>
  )
}