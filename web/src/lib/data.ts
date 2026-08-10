import type {
  Manifest,
  PracticeExamsPayload,
  StudyPacksPayload,
  TrackData,
  TrackId,
} from '../types/domain'

const dataUrl = (path: string) => `${import.meta.env.BASE_URL}data/${path}`

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(dataUrl(path))
  if (!response.ok) {
    throw new Error(`Failed to load ${path}: ${response.status} ${response.statusText}`)
  }
  return (await response.json()) as T
}

let manifestPromise: Promise<Manifest> | null = null

export function loadManifest(): Promise<Manifest> {
  manifestPromise ??= fetchJson<Manifest>('manifest.json')
  return manifestPromise
}

const trackDataCache = new Map<TrackId, Promise<TrackData>>()

export function loadTrackData(trackId: TrackId): Promise<TrackData> {
  const cached = trackDataCache.get(trackId)
  if (cached) return cached

  const promise = (async () => {
    const [manifest, examsPayload, packsPayload] = await Promise.all([
      loadManifest(),
      fetchJson<PracticeExamsPayload>(`${trackId}/practice_exams.json`),
      fetchJson<StudyPacksPayload>(`${trackId}/study_packs.json`),
    ])
    const info = manifest.tracks.find((track) => track.id === trackId)
    if (!info) throw new Error(`Unknown track '${trackId}' in manifest.json`)
    return {
      info,
      studyPacks: packsPayload.study_packs,
      fullExams: examsPayload.practice_exams,
      shortExams: examsPayload.short_practice_exams,
    }
  })()

  trackDataCache.set(trackId, promise)
  return promise
}
