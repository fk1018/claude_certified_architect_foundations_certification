import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { useOutletContext } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'

export function NotesPage() {
  const { trackData } = useOutletContext<TrackOutletContext>()
  const studyPack = trackData.studyPacks[0]
  const [activeId, setActiveId] = useState(studyPack?.notes_sections[0]?.id)

  if (!studyPack) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-10">
        <p className="text-bone-dim">No study pack available for this track yet.</p>
      </main>
    )
  }

  const activeSection =
    studyPack.notes_sections.find((section) => section.id === activeId) ??
    studyPack.notes_sections[0]

  return (
    <main className="mx-auto max-w-5xl px-6 py-10">
      <p className="font-mono text-xs uppercase tracking-[0.3em] text-brass">study pack</p>
      <h1 className="mt-2 font-display text-3xl font-semibold text-bone">{studyPack.title}</h1>

      <div className="mt-8 grid gap-6 lg:grid-cols-[220px_1fr]">
        <nav className="flex gap-2 overflow-x-auto lg:flex-col lg:overflow-visible">
          {studyPack.notes_sections.map((section) => (
            <button
              key={section.id}
              type="button"
              onClick={() => setActiveId(section.id)}
              className={`shrink-0 rounded px-3 py-2 text-left font-mono text-xs uppercase tracking-wide transition-colors ${
                section.id === activeSection?.id
                  ? 'bg-ink-3 text-brass'
                  : 'text-bone-dim hover:text-bone'
              }`}
            >
              {section.title}
            </button>
          ))}
        </nav>

        {activeSection && (
          <article className="ticket min-w-0 px-6 py-6">
            <h2 className="font-display text-xl font-semibold text-bone">
              {activeSection.title}
            </h2>
            <div className="prose-notes mt-4 text-sm leading-relaxed text-bone-dim">
              <ReactMarkdown>{activeSection.body}</ReactMarkdown>
            </div>
          </article>
        )}
      </div>
    </main>
  )
}
