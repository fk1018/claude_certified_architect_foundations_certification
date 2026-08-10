import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { loadManifest, loadTrackData } from '../lib/data'
import type { TrackInfo } from '../types/domain'

interface TrackSummary extends TrackInfo {
  examCount: number | null
  questionCount: number | null
}

export function TrackPickerPage() {
  const [summaries, setSummaries] = useState<TrackSummary[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    loadManifest()
      .then(async (manifest) => {
        const withCounts = await Promise.all(
          manifest.tracks.map(async (track) => {
            try {
              const data = await loadTrackData(track.id)
              return {
                ...track,
                examCount: data.fullExams.length,
                questionCount: data.fullExams.reduce((n, exam) => n + exam.questions.length, 0),
              }
            } catch {
              return { ...track, examCount: null, questionCount: null }
            }
          }),
        )
        if (!cancelled) setSummaries(withCounts)
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err))
      })
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="min-h-screen">
      <header className="border-b border-bone/10">
        <div className="mx-auto max-w-4xl px-6 py-5">
          <span className="font-mono text-xs tracking-[0.2em] text-brass uppercase">
            ccafc-web
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-14">
        <p className="font-mono text-xs uppercase tracking-[0.3em] text-brass">
          admissions desk
        </p>
        <h1 className="mt-3 font-display text-4xl font-semibold text-bone sm:text-5xl">
          Pick up your exam ticket.
        </h1>
        <p className="mt-4 max-w-xl text-bone-dim">
          Three certification tracks, each with a full practice-exam bank and study pack.
          Choose one to see its exams, flashcards, and notes.
        </p>

        {error && (
          <p className="mt-8 font-mono text-sm text-ember">Could not load tracks: {error}</p>
        )}

        <div className="mt-10 grid gap-5 sm:grid-cols-2">
          {(summaries ?? []).map((track, index) => (
            <Link
              key={track.id}
              to={`/${track.id}`}
              className="ticket ticket-stub group block px-6 py-5 pl-8 transition-transform hover:-translate-y-0.5"
            >
              <div className="flex items-center justify-between font-mono text-xs uppercase tracking-widest text-bone-dim">
                <span>seat {String(index + 1).padStart(2, '0')}</span>
                <span className="text-brass">{track.label}</span>
              </div>
              <h2 className="mt-3 font-display text-2xl font-semibold text-bone group-hover:text-brass-bright transition-colors">
                {track.name}
              </h2>
              <div className="mt-4 flex items-center gap-4 font-mono text-xs text-bone-dim">
                <span>
                  {track.examCount ?? '—'} exams
                </span>
                <span aria-hidden>·</span>
                <span>{track.questionCount ?? '—'} questions</span>
              </div>
            </Link>
          ))}
          {summaries === null && !error && (
            <p className="font-mono text-sm text-bone-dim">Loading tracks…</p>
          )}
        </div>
      </main>
    </div>
  )
}
