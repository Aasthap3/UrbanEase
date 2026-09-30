import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeft, LoaderCircle, LogIn } from 'lucide-react'
import { getAuthErrorMessage, useAuth } from '../context/AuthContext'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const redirect = new URLSearchParams(location.search).get('redirect') ?? '/explore'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!email.trim() || !password) {
      setError('Enter your email and password.')
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      await login({ email: email.trim(), password })
      navigate(redirect, { replace: true })
    } catch (requestError) {
      setError(getAuthErrorMessage(requestError, 'We could not sign you in. Try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100vh-80px)] max-w-md items-center px-4 py-12 sm:px-6">
      <section className="w-full rounded-3xl border border-slate-200 bg-white p-6 shadow-sm shadow-slate-200/50 sm:p-8">
        <Link to="/explore" className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"><ArrowLeft className="h-4 w-4" />Back to Explore</Link>
        <div className="mt-8 flex h-11 w-11 items-center justify-center rounded-xl bg-slate-950 text-white"><LogIn className="h-5 w-5" /></div>
        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">Welcome back</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Sign in to UrbanEase</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">Access your saved priorities and personalized accessibility score.</p>
        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-slate-700">Email<input type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          <label className="block text-sm font-medium text-slate-700">Password<input type="password" autoComplete="current-password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          {error && <p className="text-sm text-rose-700" role="alert">{error}</p>}
          <button type="submit" disabled={submitting} className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-wait disabled:opacity-60">{submitting && <LoaderCircle className="h-4 w-4 animate-spin" />}Sign In</button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-600">New to UrbanEase? <Link to={`/register?redirect=${encodeURIComponent(redirect)}`} className="font-semibold text-emerald-700 hover:text-emerald-800">Create an account</Link></p>
      </section>
    </main>
  )
}