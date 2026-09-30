import { useEffect, useState } from 'react'
import {
  ArrowRight,
  Banknote,
  BriefcaseBusiness,
  Building2,
  CheckCircle2,
  HeartPulse,
  MapPin,
  Search,
  ShieldCheck,
  TrainFront,
  TrendingUp,
  Utensils,
  Users,
} from 'lucide-react'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { ExplorePage } from './pages/ExplorePage'

const categories = [
  { name: 'Grocery', icon: <MapPin className="h-5 w-5" /> },
  { name: 'Healthcare', icon: <HeartPulse className="h-5 w-5" /> },
  { name: 'Transport', icon: <TrainFront className="h-5 w-5" /> },
  { name: 'Banking', icon: <Banknote className="h-5 w-5" /> },
  { name: 'Food', icon: <Utensils className="h-5 w-5" /> },
  { name: 'Safety', icon: <ShieldCheck className="h-5 w-5" /> },
]

const steps = [
  'Search a city, neighborhood, or landmark.',
  'Explore nearby essentials and distances.',
  'Compare neighborhoods using a personalized accessibility score.',
]

const scoreBreakdown = [
  { name: 'Grocery', value: 92 },
  { name: 'Healthcare', value: 81 },
  { name: 'Transport', value: 94 },
  { name: 'Banking', value: 88 },
  { name: 'Food', value: 84 },
]

function App() {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking')

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    fetch(`${apiUrl}/api/health`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Health check failed')
        }
        return response.json()
      })
      .then(() => setBackendStatus('online'))
      .catch(() => setBackendStatus('offline'))
  }, [])

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-stone-50 text-slate-900">
        <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/80 backdrop-blur-sm">
          <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
            <Link to="/" className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-900 text-sm font-semibold text-white">
                U
              </div>
              <div>
                <div className="text-lg font-semibold tracking-tight">UrbanEase</div>
              </div>
            </Link>

            <div className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
              <Link to="/explore" className="transition hover:text-slate-900">Explore</Link>
              <Link to="/compare" className="transition hover:text-slate-900">Compare</Link>
              <Link to="/recommend" className="transition hover:text-slate-900">Recommendations</Link>
            </div>

            <div className="flex items-center gap-3">
              <Link
                to="/login"
                className="hidden rounded-full border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-400 md:inline-flex"
              >
                Log in
              </Link>
              <Link
                to="/explore"
                className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-slate-800"
              >
                Explore now
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </nav>
        </header>

        <Routes>
          <Route
            path="/"
            element={
              <main>
                <section className="mx-auto max-w-7xl px-4 pb-20 pt-12 sm:px-6 lg:px-8 lg:pt-20">
                  <div className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
                    <div>
                      <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.12em] text-emerald-700">
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        Live neighborhood insights
                      </div>

                      <h1 className="max-w-xl text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl">
                        Everything you need, closer to where you live.
                      </h1>

                      <p className="mt-6 max-w-xl text-lg text-slate-600">
                        UrbanEase helps residents and movers judge how accessible a neighborhood really is based on essentials, everyday routines, and personal priorities.
                      </p>

                      <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                        <div className="flex w-full max-w-xl items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-200/60">
                          <Search className="h-5 w-5 text-slate-400" />
                          <input
                            type="text"
                            value="Arera Colony, Bhopal"
                            readOnly
                            className="w-full border-0 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                            aria-label="Example neighborhood search"
                          />
                        </div>
                        <Link
                          to="/explore"
                          className="inline-flex items-center justify-center rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-500"
                        >
                          Search area
                        </Link>
                      </div>

                      <div className="mt-6 flex items-center gap-3 text-sm text-slate-600">
                        <div className="flex items-center gap-2">
                          <span
                            className={`h-2.5 w-2.5 rounded-full ${
                              backendStatus === 'online'
                                ? 'bg-emerald-500'
                                : backendStatus === 'offline'
                                  ? 'bg-amber-500'
                                  : 'bg-slate-400'
                            }`}
                          />
                          <span>
                            {backendStatus === 'online'
                              ? 'Backend connected'
                              : backendStatus === 'offline'
                                ? 'Backend not reachable'
                                : 'Checking backend connection...'}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="rounded-[28px] border border-slate-200 bg-slate-900 p-5 text-white shadow-2xl shadow-slate-200/70">
                      <div className="mb-5 flex items-center justify-between">
                        <div>
                          <p className="text-xs uppercase tracking-[0.12em] text-slate-300">UrbanEase Score</p>
                          <div className="mt-2 flex items-end gap-2">
                            <span className="text-5xl font-semibold tracking-tight">86</span>
                            <span className="pb-2 text-base text-slate-300">/ 100</span>
                          </div>
                        </div>
                        <div className="rounded-2xl bg-emerald-500/15 px-3 py-2 text-sm font-medium text-emerald-300">
                          Excellent accessibility
                        </div>
                      </div>

                      <div className="space-y-4">
                        {scoreBreakdown.map((item) => (
                          <div key={item.name}>
                            <div className="mb-1 flex items-center justify-between text-sm text-slate-200">
                              <span>{item.name}</span>
                              <span>{item.value}</span>
                            </div>
                            <div className="h-2 rounded-full bg-slate-700">
                              <div
                                className="h-2 rounded-full bg-linear-to-r from-emerald-400 to-teal-300"
                                style={{ width: `${item.value}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </section>

                <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                  <div className="mb-8 flex items-end justify-between gap-4">
                    <div>
                      <p className="text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">Key categories</p>
                      <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">Everyday essentials nearby</h2>
                    </div>
                  </div>
                  <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
                    {categories.map((category) => (
                      <div
                        key={category.name}
                        className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm shadow-slate-200/40"
                      >
                        <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-slate-700">
                          {category.icon}
                        </div>
                        <h3 className="text-base font-semibold text-slate-900">{category.name}</h3>
                      </div>
                    ))}
                  </div>
                </section>

                <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
                  <div className="grid gap-10 lg:grid-cols-2">
                    <div>
                      <p className="text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">How it works</p>
                      <h2 className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">A cleaner way to judge a neighborhood</h2>
                      <div className="mt-8 space-y-5">
                        {steps.map((step, index) => (
                          <div key={step} className="flex gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm shadow-slate-200/40">
                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-sm font-semibold text-white">
                              {index + 1}
                            </div>
                            <p className="pt-2 text-slate-700">{step}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-200/40">
                      <div className="mb-4 flex items-center gap-3">
                        <TrendingUp className="h-10 w-10 rounded-xl bg-emerald-100 p-2 text-emerald-700" />
                        <div>
                          <p className="text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">UrbanEase Score</p>
                          <h3 className="text-xl font-semibold text-slate-900">Personalized accessibility</h3>
                        </div>
                      </div>

                      <p className="text-slate-600">
                        The score combines walking distance, amenity density, personal weighting, and distance decay to estimate how convenient a place is for your daily routine.
                      </p>

                      <div className="mt-6 space-y-4 border-t border-slate-200 pt-6">
                        <div className="flex items-center gap-3">
                          <Building2 className="h-5 w-5 text-slate-500" />
                          <span>Measured using real amenities and geospatial distance.</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <Users className="h-5 w-5 text-slate-500" />
                          <span>Weighted by the priorities that matter most to you.</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <BriefcaseBusiness className="h-5 w-5 text-slate-500" />
                          <span>Designed for movers, families, students, and professionals.</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>

                <footer className="border-t border-slate-200 bg-white">
                  <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-8 text-sm text-slate-600 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
                    <div className="flex items-center gap-3 font-medium text-slate-900">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 text-xs font-semibold text-white">
                        U
                      </div>
                      UrbanEase
                    </div>
                    <p>Decision support for better neighborhood choices.</p>
                  </div>
                </footer>
              </main>
            }
          />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/compare" element={<PlaceholderPage title="Compare" description="Neighborhood comparison views will be added in the next phase." />} />
          <Route path="/recommend" element={<PlaceholderPage title="Find My Ideal Area" description="Recommendation matching and explainable neighborhood suggestions will be added in a later phase." />} />
          <Route path="/login" element={<PlaceholderPage title="Login" description="Authentication features begin after the database and auth phases." />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

function PlaceholderPage({ title, description }: { title: string; description: string }) {
  return (
    <main className="mx-auto max-w-5xl px-4 py-20 sm:px-6 lg:px-8">
      <div className="rounded-[28px] border border-slate-200 bg-white p-10 shadow-sm shadow-slate-200/40">
        <p className="text-sm font-semibold uppercase tracking-[0.12em] text-slate-500">UrbanEase</p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-900">{title}</h1>
        <p className="mt-5 max-w-2xl text-lg text-slate-600">{description}</p>
        <Link
          to="/"
          className="mt-8 inline-flex items-center gap-2 rounded-full bg-slate-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800"
        >
          Back to home
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </main>
  )
}

export default App
