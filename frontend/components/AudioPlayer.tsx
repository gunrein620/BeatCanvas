'use client'

import { useEffect, useRef, useState } from 'react'

interface AudioPlayerProps {
  audioUrl: string
  metadata: {
    genre: string
    mood: string
    tempo: number
    bars: number
    key: string
    scale: string
  }
}

export default function AudioPlayer({ audioUrl, metadata }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const updateTime = () => setCurrentTime(audio.currentTime)
    const updateDuration = () => setDuration(audio.duration)
    const handleEnded = () => setIsPlaying(false)
    const handlePlay = () => setIsPlaying(true)
    const handlePause = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', updateTime)
    audio.addEventListener('loadedmetadata', updateDuration)
    audio.addEventListener('ended', handleEnded)
    audio.addEventListener('play', handlePlay)
    audio.addEventListener('pause', handlePause)

    return () => {
      audio.removeEventListener('timeupdate', updateTime)
      audio.removeEventListener('loadedmetadata', updateDuration)
      audio.removeEventListener('ended', handleEnded)
      audio.removeEventListener('play', handlePlay)
      audio.removeEventListener('pause', handlePause)
    }
  }, [audioUrl])

  const togglePlay = () => {
    const audio = audioRef.current
    if (!audio) return
    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current
    if (!audio) return
    const time = parseFloat(e.target.value)
    audio.currentTime = time
    setCurrentTime(time)
  }

  const formatTime = (seconds: number) => {
    if (!isFinite(seconds)) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="neo-card backdrop-blur-sm rounded-2xl p-8 border border-cyan-500/20 animate-border-glow transition-all duration-300 hover:scale-[1.02]">
      <audio ref={audioRef} src={audioUrl} />

      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-semibold text-gradient-cyber">Your Music</h3>
        <a
          href={audioUrl}
          download={`beatcanvas-${metadata.genre}-${metadata.mood}.mp3`}
          className="px-4 py-2 bg-gradient-to-r from-cyan-600 via-sky-600 to-purple-600 hover:from-cyan-700 hover:via-sky-700 hover:to-purple-700 rounded-lg text-sm font-medium transition-all duration-300 text-white neo-button animate-gradient-shift hover:shadow-[0_0_30px_rgba(34,211,238,0.6),0_0_60px_rgba(168,85,247,0.4)] hover:scale-110"
        >
          Download MP3
        </a>
      </div>

      {/* Metadata Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
        <div className="neo-inset bg-gray-800/40 rounded-lg p-3 border border-cyan-500/10 hover:border-cyan-400/30 hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300">
          <span className="text-cyan-300/70 drop-shadow-[0_0_5px_rgba(34,211,238,0.4)]">Genre:</span>
          <span className="text-cyan-50 font-medium ml-2 drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">{metadata.genre}</span>
        </div>
        <div className="neo-inset bg-gray-800/40 rounded-lg p-3 border border-cyan-500/10 hover:border-cyan-400/30 hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300">
          <span className="text-cyan-300/70 drop-shadow-[0_0_5px_rgba(34,211,238,0.4)]">Mood:</span>
          <span className="text-cyan-50 font-medium ml-2 drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">{metadata.mood}</span>
        </div>
        <div className="neo-inset bg-gray-800/40 rounded-lg p-3 border border-cyan-500/10 hover:border-cyan-400/30 hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300">
          <span className="text-cyan-300/70 drop-shadow-[0_0_5px_rgba(34,211,238,0.4)]">Tempo:</span>
          <span className="text-cyan-50 font-medium ml-2 drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">{metadata.tempo} BPM</span>
        </div>
        <div className="neo-inset bg-gray-800/40 rounded-lg p-3 border border-cyan-500/10 hover:border-cyan-400/30 hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300">
          <span className="text-cyan-300/70 drop-shadow-[0_0_5px_rgba(34,211,238,0.4)]">Key:</span>
          <span className="text-cyan-50 font-medium ml-2 drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">{metadata.key} {metadata.scale}</span>
        </div>
      </div>

      {/* Player Controls */}
      <div className="space-y-4">
        {/* Play/Pause Button */}
        <button
          onClick={togglePlay}
          className="w-full py-4 bg-gradient-to-r from-sky-600 via-cyan-600 to-purple-600 hover:from-sky-700 hover:via-cyan-700 hover:to-purple-700 rounded-lg font-medium text-lg transition-all duration-300 text-white neo-button animate-gradient-shift hover:shadow-[0_0_40px_rgba(14,165,233,0.8),0_0_80px_rgba(168,85,247,0.6)] flex items-center justify-center gap-2 hover:scale-105 active:scale-95 glow-intense"
        >
          {isPlaying ? (
            <>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
              </svg>
              Pause
            </>
          ) : (
            <>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
              Play
            </>
          )}
        </button>

        {/* Seek Bar */}
        <div className="space-y-2">
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="w-full h-2 bg-gray-800/50 rounded-lg appearance-none cursor-pointer accent-sky-500 hover:scale-y-125 transition-transform"
            style={{
              background: `linear-gradient(to right, #0ea5e9 ${(currentTime / (duration || 1)) * 100}%, #1f2937 ${(currentTime / (duration || 1)) * 100}%)`,
              boxShadow: `0 0 20px rgba(14, 165, 233, ${(currentTime / (duration || 1)) * 0.7}), 0 0 40px rgba(168, 85, 247, ${(currentTime / (duration || 1)) * 0.3})`
            }}
          />
          <div className="flex justify-between text-sm text-cyan-200/70 font-mono animate-pulse">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
