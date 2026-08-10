import { Link } from 'react-router-dom'
import type { TrackInfo } from '../types/domain'

export function Header({ track }: { track?: TrackInfo }) {
  return (
    <header className="border-b border-bone/10">
      <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
        <Link to="/" className="group flex items-baseline gap-2">
          <span className="font-mono text-xs tracking-[0.2em] text-brass uppercase">
            ccafc-web
          </span>
          <span className="font-display text-lg font-semibold text-bone group-hover:text-brass-bright transition-colors">
            Cert Prep Desk
          </span>
        </Link>
        {track && (
          <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-widest text-bone-dim">
            <span className="rounded border border-brass/40 px-2 py-1 text-brass">
              {track.label}
            </span>
            <span className="hidden sm:inline">{track.name}</span>
          </div>
        )}
      </div>
    </header>
  )
}
