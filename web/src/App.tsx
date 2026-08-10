import { Route, Routes } from 'react-router-dom'
import { TrackLayout } from './components/TrackLayout'
import { TrackPickerPage } from './pages/TrackPickerPage'
import { TrackHomePage } from './pages/TrackHomePage'
import { NotesPage } from './pages/NotesPage'
import { FlashcardsPage } from './pages/FlashcardsPage'
import { ExamRunnerPage } from './pages/ExamRunnerPage'
import { ExamResultsPage } from './pages/ExamResultsPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<TrackPickerPage />} />
      <Route path="/:trackId" element={<TrackLayout />}>
        <Route index element={<TrackHomePage />} />
        <Route path="notes" element={<NotesPage />} />
        <Route path="flashcards" element={<FlashcardsPage />} />
        <Route path="exam/:kind/:examId" element={<ExamRunnerPage />} />
        <Route path="exam/:kind/:examId/results" element={<ExamResultsPage />} />
      </Route>
    </Routes>
  )
}
