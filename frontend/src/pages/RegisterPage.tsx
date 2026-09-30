import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeft, LoaderCircle, UserPlus } from 'lucide-react'
import { getAuthErrorMessage, useAuth } from '../context/AuthContext'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const redirect = new URLSearchParams(location.search).get('redirect') ?? '/login'
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!name.trim() || !email.trim() || !password || !confirmation) {
      setError('Complete every field.')
      return
    }
    if (password !== confirmation) {
      setError('Passwords do not match.')
      return
    }
    if (password.length < 8) {
      setError('Password must contain at least 8 characters.')
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      await register({ name: name.trim(), email: email.trim(), password })
      setSuccess(true)
      window.setTimeout(() => navigate(`/login?redirect=${encodeURIComponent(redirect)}`), 700)
    } catch (requestError) {
      setError(getAuthErrorMessage(requestError, 'We could not create your account. Try again.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-[calc(100vh-80px)] max-w-md items-center px-4 py-12 sm:px-6">
      <section className="w-full rounded-3xl border border-slate-200 bg-white p-6 shadow-sm shadow-slate-200/50 sm:p-8">
        <Link to="/explore" className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"><ArrowLeft className="h-4 w-4" />Back to Explore</Link>
        <div className="mt-8 flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-700 text-white"><UserPlus className="h-5 w-5" /></div>
        <p className="mt-6 text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">Start with your priorities</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Create your account</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">Save profile weights and make your UrbanEase Score yours.</p>
        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-slate-700">Name<input type="text" autoComplete="name" value={name} onChange={(event) => setName(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          <label className="block text-sm font-medium text-slate-700">Email<input type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          <label className="block text-sm font-medium text-slate-700">Password<input type="password" autoComplete="new-password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          <label className="block text-sm font-medium text-slate-700">Confirm password<input type="password" autoComplete="new-password" value={confirmation} onChange={(event) => setConfirmation(event.target.value)} className="mt-2 min-h-11 w-full rounded-lg border border-slate-300 px-3 outline-none focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10" /></label>
          {error && <p className="text-sm text-rose-700" role="alert">{error}</p>}
          {success && <p className="text-sm text-emerald-700" role="status">Account created successfully. Taking you to sign in...</p>}
          <button type="submit" disabled={submitting || success} className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-emerald-700 px-4 text-sm font-semibold text-white hover:bg-emerald-600 disabled:cursor-wait disabled:opacity-60">{submitting && <LoaderCircle className="h-4 w-4 animate-spin" />}Create Account</button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-600">Already registered? <Link to={`/login?redirect=${encodeURIComponent(redirect)}`} className="font-semibold text-emerald-700 hover:text-emerald-800">Sign in</Link></p>
      </section>
    </main>
  )
}