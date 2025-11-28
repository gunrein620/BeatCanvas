/**
 * API client for BeatCanvas backend
 */

import { GenerateMusicParams } from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export interface GenerateMusicResponse {
  blob: Blob
  metadata: {
    tempo: number
    bars: number
    key: string
    scale: string
  }
}

/**
 * Generate music from genre, mood, tempo, and bars
 */
export async function generateMusic(params: GenerateMusicParams): Promise<GenerateMusicResponse> {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Failed to generate music: ${errorText}`)
  }

  // Extract metadata from headers
  const tempo = parseInt(response.headers.get('X-Tempo') || '120')
  const bars = parseInt(response.headers.get('X-Bars') || params.bars.toString())
  const key = response.headers.get('X-Key') || 'C'
  const scale = response.headers.get('X-Scale') || 'major'

  // Get MP3 blob
  const blob = await response.blob()

  return {
    blob,
    metadata: {
      tempo,
      bars,
      key,
      scale
    }
  }
}

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`)

  if (!response.ok) {
    throw new Error('Health check failed')
  }

  return await response.json()
}
