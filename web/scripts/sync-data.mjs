// Copies the CLI's already-generated exam/study-pack JSON into web/public/data/<track>/
// so the web app can fetch it as static assets at runtime. No backend involved: the CLI's
// markdown -> JSON step (cli/src/ccafc_cli/storage.py::generate_data) remains the single
// source of truth; this script just relocates its output for the browser to consume.
import { existsSync, mkdirSync, copyFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const repoRoot = path.resolve(__dirname, '..', '..')
const generatedRoot = path.join(repoRoot, 'cli', 'data', 'generated')
const publicDataRoot = path.join(__dirname, '..', 'public', 'data')

// Mirrors cli/src/ccafc_cli/paths.py::TRACK_INFO — kept in sync by hand since the CLI's
// version is the source of truth and rarely changes.
const tracks = [
  {
    id: 'architect-foundations',
    label: 'CCAFC',
    name: 'Claude Certified Architect Foundations',
    sourceDir: generatedRoot,
  },
  {
    id: 'developer-foundations',
    label: 'CCDVF',
    name: 'Claude Certified Developer Foundations',
    sourceDir: path.join(generatedRoot, 'developer-foundations'),
  },
  {
    id: 'architect-professional',
    label: 'CCARP',
    name: 'Claude Certified Architect Professional',
    sourceDir: path.join(generatedRoot, 'architect-professional'),
  },
]

const files = ['practice_exams.json', 'study_packs.json']

let copied = 0
for (const track of tracks) {
  const destDir = path.join(publicDataRoot, track.id)
  mkdirSync(destDir, { recursive: true })
  for (const file of files) {
    const src = path.join(track.sourceDir, file)
    const dest = path.join(destDir, file)
    if (!existsSync(src)) {
      throw new Error(
        `Missing ${src}. Run the CLI's data generator first, e.g.:\n` +
          `  cd cli && CCAFC_TRACK=${track.id} PYTHONPATH=src python -c "from ccafc_cli.storage import generate_data; print(generate_data())"`,
      )
    }
    copyFileSync(src, dest)
    copied += 1
  }
}

writeFileSync(
  path.join(publicDataRoot, 'manifest.json'),
  JSON.stringify(
    { tracks: tracks.map(({ id, label, name }) => ({ id, label, name })) },
    null,
    2,
  ) + '\n',
)

console.log(`Synced ${copied} data files for ${tracks.length} tracks into web/public/data/`)
