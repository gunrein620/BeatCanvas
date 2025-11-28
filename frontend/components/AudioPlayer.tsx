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
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-gray-700">
      <audio ref={audioRef} src={audioUrl} />

      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-semibold text-gray-200">Your Music</h3>
        <a
          href={audioUrl}
          download={`beatcanvas-${metadata.genre}-${metadata.mood}.mp3`}
          className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-sm font-medium transition text-white"
        >
          Download MP3
        </a>
      </div>

      {/* Metadata Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
        <div className="bg-gray-700/50 rounded-lg p-3">
          <span className="text-gray-400">Genre:</span>
          <span className="text-white font-medium ml-2">{metadata.genre}</span>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-3">
          <span className="text-gray-400">Mood:</span>
          <span className="text-white font-medium ml-2">{metadata.mood}</span>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-3">
          <span className="text-gray-400">Tempo:</span>
          <span className="text-white font-medium ml-2">{metadata.tempo} BPM</span>
        </div>
        <div className="bg-gray-700/50 rounded-lg p-3">
          <span className="text-gray-400">Key:</span>
          <span className="text-white font-medium ml-2">{metadata.key} {metadata.scale}</span>
        </div>
      </div>

      {/* Player Controls */}
      <div className="space-y-4">
        {/* Play/Pause Button */}
        <button
          onClick={togglePlay}
          className="w-full py-4 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium text-lg transition text-white flex items-center justify-center gap-2"
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
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
            style={{
              background: `linear-gradient(to right, #9333ea ${(currentTime / (duration || 1)) * 100}%, #374151 ${(currentTime / (duration || 1)) * 100}%)`
            }}
          />
          <div className="flex justify-between text-sm text-gray-400">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
