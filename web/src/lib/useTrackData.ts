import { useEffect, useState } from 'react'
import { loadTrackData } from './data'
import type { TrackData, TrackId } from '../types/domain'

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; data: TrackData }

export function useTrackData(trackId: TrackId | undefined): State {
  const [state, setState] = useState<State>({ status: 'loading' })

  useEffect(() => {
    if (!trackId) return
    setState({ status: 'loading' })
    let cancelled = false
    loadTrackData(trackId)
      .then((data) => {
        if (!cancelled) setState({ status: 'ready', data })
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setState({
            status: 'error',
            message: error instanceof Error ? error.message : String(error),
          })
        }
      })
    return () => {
      cancelled = true
    }
  }, [trackId])

  return state
}
