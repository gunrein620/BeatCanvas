'use client'

import { useState } from 'react'
import PromptForm from '@/components/PromptForm'
import AudioPlayer from '@/components/AudioPlayer'
import MusicHistory from '@/components/MusicHistory'
import { generateMusic } from '@/lib/api'
import { saveToHistory } from '@/lib/storage'
import { HistoryEntry } from '@/lib/types'

export default function Home() {
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [metadata, setMetadata] = useState<{
    genre: string
    mood: string
    tempo: number
    bars: number
    key: string
    scale: string
  } | null>(null)

  const handleGenerate = async (genre: string, mood: string, tempo?: number, bars: number = 8) => {
    console.log('=== GENERATE REQUEST ===')
    console.log('Genre:', genre)
    console.log('Mood:', mood)
    console.log('Tempo:', tempo)
    console.log('Bars:', bars)
    console.log('========================')

    setIsGenerating(true)
    setError(null)
    setAudioUrl(null)
    setMetadata(null)

    try {
      const result = await generateMusic({
        genre,
        mood,
        tempo,
        bars
      })

      console.log('=== RECEIVED RESPONSE ===')
      console.log('Metadata:', result.metadata)
      console.log('Blob size:', result.blob.size)
      console.log('=========================')

      const url = URL.createObjectURL(result.blob)
      const musicMetadata = {
        genre,
        mood,
        ...result.metadata,
        timestamp: Date.now()
      }

      setAudioUrl(url)
      setMetadata(musicMetadata)

      // Save to history
      saveToHistory(musicMetadata, result.blob)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate music')
      console.error('Generation error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const handlePlayFromHistory = (entry: HistoryEntry) => {
    setAudioUrl(entry.audioUrl)
    setMetadata(entry.metadata)
    setError(null)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <div className="container mx-auto px-4 py-16 max-w-2xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
            BeatCanvas
          </h1>
          <p className="text-gray-400 text-lg">
            AI-powered 8-bar music loop generator
          </p>
        </div>

        {/* Form */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-gray-700 mb-8">
          <PromptForm onSubmit={handleGenerate} isLoading={isGenerating} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-900/50 border border-red-500 rounded-lg p-4 mb-8">
            <p className="text-red-200 text-center">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {isGenerating && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-purple-500 mb-4"></div>
            <p className="text-gray-400 text-lg">Generating your music...</p>
            <p className="text-gray-500 text-sm mt-2">This may take 10-20 seconds</p>
          </div>
        )}

        {/* Audio Player */}
        {audioUrl && metadata && !isGenerating && (
          <AudioPlayer audioUrl={audioUrl} metadata={metadata} />
        )}

        {/* Music History */}
        <MusicHistory onPlay={handlePlayFromHistory} />
      </div>
    </main>
  )
}
