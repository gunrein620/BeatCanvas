'use client'

import { useEffect, useState } from 'react'
import { HistoryEntry } from '@/lib/types'
import { getHistory, deleteFromHistory, clearHistory } from '@/lib/storage'

interface MusicHistoryProps {
  onPlay: (entry: HistoryEntry) => void
}

export default function MusicHistory({ onPlay }: MusicHistoryProps) {
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [isExpanded, setIsExpanded] = useState(false)

  // Load history on mount
  useEffect(() => {
    setHistory(getHistory())
  }, [])

  const handleDelete = (id: string) => {
    deleteFromHistory(id)
    setHistory(getHistory())
  }

  const handleClearAll = () => {
    if (confirm('Are you sure you want to clear all history?')) {
      clearHistory()
      setHistory([])
    }
  }

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`
    return date.toLocaleDateString()
  }

  if (history.length === 0) {
    return null
  }

  return (
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-6 shadow-2xl border border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 text-lg font-semibold text-gray-200 hover:text-white transition"
        >
          <svg
            className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
          </svg>
          History ({history.length})
        </button>
        {isExpanded && history.length > 0 && (
          <button
            onClick={handleClearAll}
            className="text-sm text-red-400 hover:text-red-300 transition"
          >
            Clear All
          </button>
        )}
      </div>

      {/* History List */}
      {isExpanded && (
        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
          {history.map((entry) => (
            <div
              key={entry.id}
              className="bg-gray-700/50 rounded-lg p-4 hover:bg-gray-700 transition"
            >
              <div className="flex items-center justify-between gap-4">
                {/* Metadata */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-white">{entry.metadata.genre}</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-gray-300">{entry.metadata.mood}</span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-gray-400">
                    <span>{entry.metadata.tempo} BPM</span>
                    <span>•</span>
                    <span>{entry.metadata.bars} bars</span>
                    <span>•</span>
                    <span>{entry.metadata.key} {entry.metadata.scale}</span>
                    <span>•</span>
                    <span>{formatDate(entry.metadata.timestamp)}</span>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onPlay(entry)}
                    className="p-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition"
                    title="Play"
                  >
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => handleDelete(entry.id)}
                    className="p-2 bg-red-600/50 hover:bg-red-600 rounded-lg transition"
                    title="Delete"
                  >
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
