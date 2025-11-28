"""
Pydantic models for request/response validation and music data structures.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


# ===== Request/Response Models =====

class GenerateRequest(BaseModel):
    """Request model for /api/generate endpoint."""

    genre: str = Field(..., min_length=1, max_length=50, description="Music genre (e.g., EDM, Jazz, Hip-Hop)")
    mood: str = Field(..., min_length=1, max_length=50, description="Music mood (e.g., Happy, Sad, Energetic)")
    tempo: Optional[int] = Field(None, ge=60, le=180, description="BPM (60-180), AI selects if not provided")
    bars: int = Field(default=8, ge=4, le=16, description="Number of bars (4, 8, or 16)")

    class Config:
        json_schema_extra = {
            "example": {
                "genre": "EDM",
                "mood": "Energetic",
                "tempo": 128,
                "bars": 8
            }
        }


# ===== Music JSON Schema Models =====

class NoteSchema(BaseModel):
    """Represents a single musical note."""

    pitch: int = Field(..., ge=0, le=127, description="MIDI note number (0-127)")
    start_time: float = Field(..., ge=0, description="Start time in quarter notes")
    duration: float = Field(..., gt=0, le=16, description="Duration in quarter notes")
    velocity: int = Field(..., ge=0, le=127, description="Note velocity/volume (0-127)")

    class Config:
        json_schema_extra = {
            "example": {
                "pitch": 60,
                "start_time": 0.0,
                "duration": 1.0,
                "velocity": 100
            }
        }


class TrackSchema(BaseModel):
    """Represents a single instrument track."""

    name: str = Field(..., description="Track name (e.g., drums, bass, melody)")
    instrument: str = Field(..., description="Instrument type")
    midi_program: int = Field(..., ge=0, le=127, description="MIDI program number (0-127)")
    notes: List[NoteSchema] = Field(..., description="List of notes in this track")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "drums",
                "instrument": "drums",
                "midi_program": 0,
                "notes": [
                    {
                        "pitch": 36,
                        "start_time": 0.0,
                        "duration": 0.25,
                        "velocity": 100
                    }
                ]
            }
        }


class MetadataSchema(BaseModel):
    """Metadata for the music composition."""

    tempo: int = Field(..., ge=60, le=200, description="Tempo in BPM (60-200)")
    bars: int = Field(..., ge=4, le=16, description="Number of bars (4, 8, or 16)")
    time_signature: List[int] = Field(default=[4, 4], description="Time signature [numerator, denominator]")
    key: str = Field(..., pattern="^[A-G](#|b)?$", description="Root key (C, D, E, F, G, A, B, with optional # or b)")
    scale: Literal["major", "minor"] = Field(..., description="Scale type")

    class Config:
        json_schema_extra = {
            "example": {
                "tempo": 120,
                "bars": 8,
                "time_signature": [4, 4],
                "key": "C",
                "scale": "major"
            }
        }


class MusicSchema(BaseModel):
    """Complete music composition schema."""

    metadata: MetadataSchema = Field(..., description="Composition metadata")
    tracks: List[TrackSchema] = Field(..., min_length=1, description="List of instrument tracks")

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "tempo": 120,
                    "bars": 8,
                    "time_signature": [4, 4],
                    "key": "C",
                    "scale": "major"
                },
                "tracks": [
                    {
                        "name": "drums",
                        "instrument": "drums",
                        "midi_program": 0,
                        "notes": [
                            {
                                "pitch": 36,
                                "start_time": 0.0,
                                "duration": 0.25,
                                "velocity": 100
                            }
                        ]
                    }
                ]
            }
        }
