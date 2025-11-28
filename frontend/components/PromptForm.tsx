'use client'

import { useState } from 'react'

interface PromptFormProps {
  onSubmit: (genre: string, mood: string, tempo?: number, bars?: number) => void
  isLoading: boolean
}

export default function PromptForm({ onSubmit, isLoading }: PromptFormProps) {
  const [genre, setGenre] = useState('')
  const [mood, setMood] = useState('')
  const [tempo, setTempo] = useState<number | undefined>(undefined)
  const [useTempo, setUseTempo] = useState(false)
  const [bars, setBars] = useState<4 | 8 | 16>(8)

  const genrePresets = ['EDM', 'Hip-Hop', 'Jazz', 'Rock', 'Ambient']
  const moodPresets = ['Happy', 'Sad', 'Energetic', 'Calm', 'Dark']

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (genre.trim() && mood.trim()) {
      onSubmit(genre.trim(), mood.trim(), useTempo ? tempo : undefined, bars)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Genre Input */}
      <div>
        <label htmlFor="genre" className="block text-sm font-medium mb-2 text-gray-200">
          Genre
        </label>
        <input
          type="text"
          id="genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          placeholder="e.g., EDM, Jazz, Hip-Hop"
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          disabled={isLoading}
          required
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {genrePresets.map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => setGenre(preset)}
              className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded-full transition text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {preset}
            </button>
          ))}
        </div>
      </div>

      {/* Mood Input */}
      <div>
        <label htmlFor="mood" className="block text-sm font-medium mb-2 text-gray-200">
          Mood
        </label>
        <input
          type="text"
          id="mood"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          placeholder="e.g., Energetic, Calm, Dark"
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          disabled={isLoading}
          required
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {moodPresets.map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => setMood(preset)}
              className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded-full transition text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {preset}
            </button>
          ))}
        </div>
      </div>

      {/* BPM Control */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-medium text-gray-200">
            Tempo (BPM)
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-400">
            <input
              type="checkbox"
              checked={useTempo}
              onChange={(e) => {
                setUseTempo(e.target.checked)
                if (!tempo) setTempo(120)
              }}
              disabled={isLoading}
              className="rounded bg-gray-700 border-gray-600 text-purple-600 focus:ring-purple-500"
            />
            Specify tempo
          </label>
        </div>
        {useTempo ? (
          <>
            <div className="flex items-center gap-4">
              <input
                type="range"
                min="60"
                max="180"
                value={tempo || 120}
                onChange={(e) => setTempo(parseInt(e.target.value))}
                disabled={isLoading}
                className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
              />
              <input
                type="number"
                min="60"
                max="180"
                value={tempo || 120}
                onChange={(e) => setTempo(parseInt(e.target.value))}
                disabled={isLoading}
                className="w-20 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-center text-white focus:ring-2 focus:ring-purple-500 outline-none"
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">60 (slow) - 180 (fast) BPM</p>
          </>
        ) : (
          <p className="text-sm text-gray-500 py-3">
            AI will select tempo based on genre
          </p>
        )}
      </div>

      {/* Bars Selector */}
      <div>
        <label className="block text-sm font-medium mb-3 text-gray-200">
          Music Length
        </label>
        <div className="grid grid-cols-3 gap-3">
          {([4, 8, 16] as const).map((barOption) => (
            <button
              key={barOption}
              type="button"
              onClick={() => setBars(barOption)}
              disabled={isLoading}
              className={`py-3 px-4 rounded-lg font-medium transition ${
                bars === barOption
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {barOption} bars
            </button>
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-2">
          {bars === 4 && '~8 seconds'}
          {bars === 8 && '~16 seconds'}
          {bars === 16 && '~32 seconds'}
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !genre.trim() || !mood.trim()}
        className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed rounded-lg font-semibold text-lg transition text-white"
      >
        {isLoading ? 'Generating...' : 'Generate Music'}
      </button>
    </form>
  )
}
