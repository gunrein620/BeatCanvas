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
        <label htmlFor="genre" className="block text-sm font-medium mb-2 text-cyan-100 tracking-wide drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]">
          Genre
        </label>
        <input
          type="text"
          id="genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          placeholder="e.g., EDM, Jazz, Hip-Hop"
          className="w-full px-4 py-3 neo-inset bg-gray-900/50 border border-cyan-500/30 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-400 focus:shadow-[0_0_30px_rgba(14,165,233,0.6)] focus:scale-[1.01] outline-none text-cyan-50 placeholder-cyan-400/40 transition-all duration-300"
          disabled={isLoading}
          required
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {genrePresets.map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => setGenre(preset)}
              className="px-3 py-1 text-sm neo-button bg-gray-800/80 hover:bg-gray-700/90 hover:shadow-[0_0_20px_rgba(34,211,238,0.6)] hover:scale-110 hover:rotate-1 rounded-full transition-all duration-300 text-cyan-100 border border-cyan-500/20 hover:border-cyan-400/60 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
            >
              {preset}
            </button>
          ))}
        </div>
      </div>

      {/* Mood Input */}
      <div>
        <label htmlFor="mood" className="block text-sm font-medium mb-2 text-cyan-100 tracking-wide drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]">
          Mood
        </label>
        <input
          type="text"
          id="mood"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          placeholder="e.g., Energetic, Calm, Dark"
          className="w-full px-4 py-3 neo-inset bg-gray-900/50 border border-cyan-500/30 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-400 focus:shadow-[0_0_30px_rgba(14,165,233,0.6)] focus:scale-[1.01] outline-none text-cyan-50 placeholder-cyan-400/40 transition-all duration-300"
          disabled={isLoading}
          required
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {moodPresets.map((preset) => (
            <button
              key={preset}
              type="button"
              onClick={() => setMood(preset)}
              className="px-3 py-1 text-sm neo-button bg-gray-800/80 hover:bg-gray-700/90 hover:shadow-[0_0_20px_rgba(34,211,238,0.6)] hover:scale-110 hover:rotate-1 rounded-full transition-all duration-300 text-cyan-100 border border-cyan-500/20 hover:border-cyan-400/60 disabled:opacity-50 disabled:cursor-not-allowed"
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
          <label className="block text-sm font-medium text-cyan-100 tracking-wide drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]">
            Tempo (BPM)
          </label>
          <label className="flex items-center gap-2 text-sm text-cyan-200/70">
            <input
              type="checkbox"
              checked={useTempo}
              onChange={(e) => {
                setUseTempo(e.target.checked)
                if (!tempo) setTempo(120)
              }}
              disabled={isLoading}
              className="rounded bg-gray-800 border-cyan-500/30 text-sky-500 focus:ring-sky-500 checked:animate-pulse-glow"
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
                className="flex-1 h-2 bg-gray-800/50 rounded-lg appearance-none cursor-pointer accent-sky-500 hover:shadow-[0_0_20px_rgba(14,165,233,0.5)] transition-all"
              />
              <input
                type="number"
                min="60"
                max="180"
                value={tempo || 120}
                onChange={(e) => setTempo(parseInt(e.target.value))}
                disabled={isLoading}
                className="w-20 px-3 py-2 neo-inset bg-gray-900/50 border border-cyan-500/30 rounded-lg text-center text-cyan-50 focus:ring-2 focus:ring-sky-500 focus:shadow-[0_0_20px_rgba(14,165,233,0.5)] outline-none transition-all duration-300"
              />
            </div>
            <p className="text-xs text-cyan-300/50 mt-1">60 (slow) - 180 (fast) BPM</p>
          </>
        ) : (
          <p className="text-sm text-cyan-200/50 py-3">
            AI will select tempo based on genre
          </p>
        )}
      </div>

      {/* Bars Selector */}
      <div>
        <label className="block text-sm font-medium mb-3 text-cyan-100 tracking-wide drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]">
          Music Length
        </label>
        <div className="grid grid-cols-3 gap-3">
          {([4, 8, 16] as const).map((barOption) => (
            <button
              key={barOption}
              type="button"
              onClick={() => setBars(barOption)}
              disabled={isLoading}
              className={`py-3 px-4 rounded-lg font-medium transition-all duration-300 ${
                bars === barOption
                  ? 'bg-gradient-to-br from-sky-500 via-cyan-500 to-purple-500 text-white animate-gradient-shift shadow-[0_0_30px_rgba(14,165,233,0.7),0_0_60px_rgba(168,85,247,0.4)] scale-110 animate-pulse-glow'
                  : 'neo-button bg-gray-800/70 text-cyan-100 hover:bg-gray-700/80 hover:shadow-[0_0_20px_rgba(34,211,238,0.5)] hover:scale-105 border border-cyan-500/20 hover:border-cyan-400/60'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {barOption} bars
            </button>
          ))}
        </div>
        <p className="text-xs text-cyan-300/50 mt-2">
          {bars === 4 && '~8 seconds'}
          {bars === 8 && '~16 seconds'}
          {bars === 16 && '~32 seconds'}
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !genre.trim() || !mood.trim()}
        className="w-full py-4 bg-gradient-to-r from-sky-500 via-cyan-500 to-purple-500 hover:from-sky-600 hover:via-cyan-600 hover:to-purple-600 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed rounded-lg font-semibold text-lg transition-all duration-300 text-white neo-button animate-gradient-shift hover:shadow-[0_0_40px_rgba(14,165,233,0.8),0_0_80px_rgba(168,85,247,0.5)] hover:scale-105 active:scale-95 glow-intense"
      >
        {isLoading ? 'Generating...' : 'Generate Music'}
      </button>
    </form>
  )
}
