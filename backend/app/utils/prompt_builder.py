"""
Prompt Builder: Creates optimized prompts for OpenAI to generate music JSON.
"""

from typing import Optional


class PromptBuilder:
    """Builds genre/mood-aware prompts for music generation."""

    # MIDI drum map reference
    DRUM_MAP = {
        "kick": 36,
        "snare": 38,
        "closed_hi_hat": 42,
        "open_hi_hat": 46,
        "crash": 49,
        "ride": 51,
        "floor_tom": 41,
        "high_tom": 48
    }

    # Genre-specific guidelines
    GENRE_GUIDELINES = {
        "edm": {
            "tempo_range": "120-140",
            "description": "Fast tempo, four-on-floor kick pattern, synth leads, energetic"
        },
        "hip-hop": {
            "tempo_range": "80-100",
            "description": "Medium tempo, heavy bass, syncopated hi-hats, laid-back groove"
        },
        "jazz": {
            "tempo_range": "100-140",
            "description": "Swing feel, walking bass, complex harmonies, improvisation"
        },
        "rock": {
            "tempo_range": "110-130",
            "description": "Steady drums, electric guitar/bass, driving energy"
        },
        "ambient": {
            "tempo_range": "60-90",
            "description": "Slow tempo, sustained pads, minimal drums, atmospheric"
        }
    }

    # Mood-specific guidelines
    MOOD_GUIDELINES = {
        "happy": "Major key, higher velocities (90-120), busy rhythms, uplifting",
        "sad": "Minor key, lower velocities (50-80), slower movement, melancholic",
        "energetic": "Fast tempo, many notes, strong accents, driving rhythm",
        "calm": "Slow tempo, sparse notes, soft dynamics, gentle"
    }

    @staticmethod
    def build_music_generation_prompt(
        genre: str,
        mood: str,
        tempo: Optional[int] = None,
        bars: int = 8
    ) -> str:
        """
        Builds a comprehensive prompt for music generation.

        Args:
            genre: Music genre (e.g., EDM, Jazz, Hip-Hop)
            mood: Music mood (e.g., Happy, Sad, Energetic)
            tempo: Optional specific tempo (BPM). If None, AI selects based on genre
            bars: Number of bars to generate (4, 8, or 16)

        Returns:
            Formatted prompt string for OpenAI
        """
        # Normalize genre/mood for lookup
        genre_key = genre.lower().replace("-", "").replace(" ", "")
        mood_key = mood.lower()

        # Get genre-specific guidelines
        genre_info = PromptBuilder.GENRE_GUIDELINES.get(genre_key, {
            "tempo_range": "90-130",
            "description": "General music style"
        })

        # Get mood-specific guidelines
        mood_info = PromptBuilder.MOOD_GUIDELINES.get(mood_key, "Appropriate to the specified mood")

        # Calculate max quarter notes
        max_quarter_notes = bars * 4

        # Build tempo instruction
        if tempo:
            tempo_instruction = f"Use exactly {tempo} BPM as specified."
        else:
            tempo_instruction = f"Choose an appropriate tempo in the range {genre_info['tempo_range']} BPM based on the genre."

        prompt = f"""You are a music composition AI. Generate a {bars}-bar music loop in JSON format.

**Requirements:**
Genre: {genre}
Mood: {mood}
Bars: {bars} (equals {max_quarter_notes} quarter notes in 4/4 time)
{tempo_instruction}

**Musical Structure:**
1. Create 3-4 instrument tracks:
   - drums (required): Use MIDI program 0, is_drum track
   - bass (required): Use MIDI programs 32-39
   - melody (required): Use MIDI programs 0-7 (piano), 24-31 (guitar), or 80-87 (synth leads)
   - chords (optional): Use MIDI programs 0-7 (piano) or 48-55 (strings)

2. Timing:
   - All notes must have start_time between 0 and {max_quarter_notes} (quarter notes)
   - Align notes to reasonable rhythmic subdivisions (whole, half, quarter, eighth, sixteenth notes)
   - Duration should be musically appropriate (not too long or too short)

3. Genre Guidelines ({genre}):
   - {genre_info['description']}
   - Tempo range: {genre_info['tempo_range']} BPM

4. Mood Guidelines ({mood}):
   - {mood_info}

5. Key and Scale:
   - Choose an appropriate key (C, D, E, F, G, A, B, with optional # or b)
   - Use major scale for uplifting moods, minor for melancholic moods

**MIDI Drum Map (pitch values):**
- 36: Kick (bass drum)
- 38: Snare
- 42: Closed hi-hat
- 46: Open hi-hat
- 49: Crash cymbal
- 51: Ride cymbal
- 41, 43, 45: Toms (low to high)
- 48, 50: Toms (mid to high)

**Musical Coherence:**
- Create rhythmically aligned patterns that loop seamlessly
- Use appropriate note velocities (0-127) for dynamics
- Ensure bass and melody complement each other harmonically
- Make drums provide a solid rhythmic foundation

**Output Format:**
Return ONLY valid JSON with this exact structure (no additional text):

{{
  "metadata": {{
    "tempo": <integer 60-200>,
    "bars": {bars},
    "time_signature": [4, 4],
    "key": "<string>",
    "scale": "<major or minor>"
  }},
  "tracks": [
    {{
      "name": "drums",
      "instrument": "drums",
      "midi_program": 0,
      "notes": [
        {{
          "pitch": <integer 0-127>,
          "start_time": <float 0-{max_quarter_notes}>,
          "duration": <float>,
          "velocity": <integer 0-127>
        }}
      ]
    }},
    {{
      "name": "bass",
      "instrument": "<bass instrument>",
      "midi_program": <integer 32-39>,
      "notes": [...]
    }},
    {{
      "name": "melody",
      "instrument": "<melodic instrument>",
      "midi_program": <integer>,
      "notes": [...]
    }}
  ]
}}

Generate musically coherent, genre-appropriate, and mood-fitting composition. Output valid JSON only."""

        return prompt


# Example usage
if __name__ == "__main__":
    builder = PromptBuilder()

    # Test prompt generation
    prompt = builder.build_music_generation_prompt(
        genre="EDM",
        mood="Energetic",
        tempo=128,
        bars=8
    )

    print("Generated Prompt:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
    print(f"\nPrompt length: {len(prompt)} characters")
