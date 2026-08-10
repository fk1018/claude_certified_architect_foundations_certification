import { Navigate, Outlet, useParams } from 'react-router-dom'
import { Header } from './Header'
import { useTrackData } from '../lib/useTrackData'
import { isTrackId } from '../lib/tracks'
import type { TrackData } from '../types/domain'

export interface TrackOutletContext {
  trackData: TrackData
}

export function TrackLayout() {
  const { trackId } = useParams<{ trackId: string }>()
  const valid = isTrackId(trackId)
  // Hooks must run unconditionally on every render — react-router reuses this
  // component instance across sibling "/:trackId" routes, so an early return
  // before this call would violate the rules of hooks the moment someone
  // navigates from a valid track straight to an invalid one.
  const state = useTrackData(valid ? trackId : undefined)

  if (!valid) {
    return <Navigate to="/" replace />
  }

  if (state.status === 'loading') {
    return (
      <div className="min-h-screen">
        <Header />
        <div className="mx-auto max-w-4xl px-6 py-16 text-center font-mono text-sm text-bone-dim">
          Loading {trackId}…
        </div>
      </div>
    )
  }

  if (state.status === 'error') {
    return (
      <div className="min-h-screen">
        <Header />
        <div className="mx-auto max-w-4xl px-6 py-16 text-center">
          <p className="font-display text-xl text-ember">Could not load this track.</p>
          <p className="mt-2 font-mono text-sm text-bone-dim">{state.message}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <Header track={state.data.info} />
      <Outlet context={{ trackData: state.data } satisfies TrackOutletContext} />
    </div>
  )
}
