import { useMemo, useState } from 'react'
import { useOutletContext, useParams } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'
import { loadProgress, setFlashcardKnown } from '../lib/progress'
import type { TrackId } from '../types/domain'

export function FlashcardsPage() {
  const { trackId } = useParams<{ trackId: TrackId }>()
  const { trackData } = useOutletContext<TrackOutletContext>()
  const cards = trackData.studyPacks[0]?.flashcards ?? []

  const [progressVersion, setProgressVersion] = useState(0)
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [onlyUnknown, setOnlyUnknown] = useState(false)

  const progress = useMemo(
    () => loadProgress(trackId as TrackId),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [trackId, progressVersion],
  )

  const visibleCards = onlyUnknown
    ? cards.filter((card) => !progress.flashcards[card.id]?.known)
    : cards

  const card = visibleCards[Math.min(index, Math.max(visibleCards.length - 1, 0))]
  const knownCount = cards.filter((c) => progress.flashcards[c.id]?.known).length

  function goto(delta: number) {
    setFlipped(false)
    setIndex((current) => {
      const next = current + delta
      if (next < 0) return Math.max(visibleCards.length - 1, 0)
      if (next >= visibleCards.length) return 0
      return next
    })
  }

  function markKnown(known: boolean) {
    if (!card || !trackId) return
    setFlashcardKnown(trackId as TrackId, card.id, known)
    setProgressVersion((v) => v + 1)
    goto(1)
  }

  if (cards.length === 0) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-10">
        <p className="text-bone-dim">No flashcards available for this track yet.</p>
      </main>
    )
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <div className="flex items-center justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.3em] text-brass">flashcards</p>
          <p className="mt-1 font-mono text-xs text-bone-dim">
            {knownCount}/{cards.length} known
          </p>
        </div>
        <label className="flex items-center gap-2 font-mono text-xs uppercase tracking-wide text-bone-dim">
          <input
            type="checkbox"
            checked={onlyUnknown}
            onChange={(event) => {
              setOnlyUnknown(event.target.checked)
              setIndex(0)
              setFlipped(false)
            }}
            className="accent-brass"
          />
          unknown only
        </label>
      </div>

      {visibleCards.length === 0 ? (
        <p className="mt-10 text-center font-display text-xl text-sage">
          All caught up — every card is marked known.
        </p>
      ) : (
        <>
          <button
            type="button"
            onClick={() => setFlipped((f) => !f)}
            className="ticket mt-8 flex min-h-64 w-full flex-col items-center justify-center px-8 py-10 text-center transition-transform"
          >
            <p className="font-mono text-[11px] uppercase tracking-widest text-brass">
              {card.topic} · {flipped ? 'answer' : 'question'}
            </p>
            <p className="mt-4 font-display text-xl text-bone">
              {flipped ? card.answer : card.question}
            </p>
            <p className="mt-6 font-mono text-[11px] uppercase tracking-widest text-bone-dim/60">
              tap to {flipped ? 'see question' : 'reveal answer'}
            </p>
          </button>

          <div className="mt-6 flex items-center justify-between">
            <button
              type="button"
              onClick={() => goto(-1)}
              className="font-mono text-sm text-bone-dim hover:text-bone"
            >
              ← prev
            </button>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => markKnown(false)}
                className="rounded border border-ember/40 px-4 py-2 font-mono text-xs uppercase tracking-wide text-ember hover:bg-ember/10"
              >
                still learning
              </button>
              <button
                type="button"
                onClick={() => markKnown(true)}
                className="rounded border border-sage/40 px-4 py-2 font-mono text-xs uppercase tracking-wide text-sage hover:bg-sage/10"
              >
                known
              </button>
            </div>
            <button
              type="button"
              onClick={() => goto(1)}
              className="font-mono text-sm text-bone-dim hover:text-bone"
            >
              next →
            </button>
          </div>
        </>
      )}
    </main>
  )
}
