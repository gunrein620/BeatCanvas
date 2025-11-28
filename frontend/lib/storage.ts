/**
 * LocalStorage management for music history
 */

import { HistoryEntry, MusicMetadata } from './types'

const STORAGE_KEY = 'beatcanvas_history'
const MAX_HISTORY_ITEMS = 20

/**
 * Save a generated music entry to history
 */
export function saveToHistory(metadata: MusicMetadata, audioBlob: Blob): HistoryEntry {
  const history = getHistory()

  // Create blob URL
  const audioUrl = URL.createObjectURL(audioBlob)

  // Create new entry
  const entry: HistoryEntry = {
    id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    metadata,
    audioUrl
  }

  // Add to beginning of history
  history.unshift(entry)

  // Limit to MAX_HISTORY_ITEMS
  const trimmedHistory = history.slice(0, MAX_HISTORY_ITEMS)

  // Save to localStorage
  saveHistory(trimmedHistory)

  return entry
}

/**
 * Get all history entries
 */
export function getHistory(): HistoryEntry[] {
  if (typeof window === 'undefined') return []

  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return []

    const history: HistoryEntry[] = JSON.parse(stored)
    return history
  } catch (error) {
    console.error('Failed to load history:', error)
    return []
  }
}

/**
 * Delete a specific entry from history
 */
export function deleteFromHistory(id: string): void {
  const history = getHistory()
  const filtered = history.filter(entry => entry.id !== id)
  saveHistory(filtered)
}

/**
 * Clear all history
 */
export function clearHistory(): void {
  if (typeof window === 'undefined') return

  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch (error) {
    console.error('Failed to clear history:', error)
  }
}

/**
 * Save history to localStorage
 */
function saveHistory(history: HistoryEntry[]): void {
  if (typeof window === 'undefined') return

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history))
  } catch (error) {
    console.error('Failed to save history:', error)
  }
}
