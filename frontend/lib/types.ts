/**
 * TypeScript interfaces for BeatCanvas frontend
 */

export interface GenerateMusicParams {
  genre: string
  mood: string
  tempo?: number  // Optional, AI selects if not provided
  bars: number    // 4, 8, or 16
}

export interface MusicMetadata {
  genre: string
  mood: string
  tempo: number
  bars: number
  key: string
  scale: string
  timestamp: number
}

export interface HistoryEntry {
  id: string
  metadata: MusicMetadata
  audioUrl: string
}
