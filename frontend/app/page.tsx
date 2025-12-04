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
    <main className="min-h-screen bg-[var(--bg-cyber)] relative overflow-hidden">
      {/* 애니메이션 그리드 배경 */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(34,211,238,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(34,211,238,0.1)_1px,transparent_1px)] bg-[size:50px_50px] animate-[grid-move_20s_linear_infinite]"></div>
      </div>

      {/* 스캔라인 효과 */}
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-50 animate-[scanline_8s_linear_infinite]"></div>

      {/* 파티클 시스템 (50개) */}
      <div className="absolute inset-0 pointer-events-none">
        {Array.from({ length: 50 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-cyan-400 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `particle-float ${3 + Math.random() * 5}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 5}s`,
              opacity: 0.3 + Math.random() * 0.5
            }}
          />
        ))}
      </div>

      {/* 기존 컨텐츠 */}
      <div className="container mx-auto px-4 py-16 max-w-2xl relative z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold mb-4 text-gradient-cyber animate-float">
            예술과 소프트웨어
          </h1>
          <p className="text-cyan-100/80 text-lg tracking-wide animate-pulse-glow">
            AI-작곡 악상보조 프로그램
          </p>
        </div>

        {/* Form */}
        <div className="neo-card backdrop-blur-sm rounded-2xl p-8 border border-cyan-500/20 animate-border-glow mb-8 transition-all duration-300 hover:border-cyan-400/40 hover:scale-[1.01]">
          <PromptForm onSubmit={handleGenerate} isLoading={isGenerating} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="neo-inset bg-red-900/30 border border-red-400/50 rounded-lg p-4 mb-8 backdrop-blur-sm animate-pulse">
            <p className="text-red-200 text-center">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {isGenerating && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-cyan-400 mb-4 glow-intense"></div>
            <p className="text-cyan-100/70 text-lg animate-pulse">Generating your music...</p>
            <p className="text-cyan-200/50 text-sm mt-2 animate-pulse">This may take 10-20 seconds</p>
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
