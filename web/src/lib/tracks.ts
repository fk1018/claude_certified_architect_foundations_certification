import type { TrackId } from '../types/domain'

export const TRACK_IDS: TrackId[] = [
  'architect-foundations',
  'developer-foundations',
  'architect-professional',
]

export function isTrackId(value: string | undefined): value is TrackId {
  return !!value && (TRACK_IDS as string[]).includes(value)
}
