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

    # Genre-specific guidelines (expanded with harmonic progressions)
    GENRE_GUIDELINES = {
        "edm": {
            "tempo_range": "120-140",
            "harmonic_progressions": "I-V-vi-IV, I-vi-IV-V (pop progressions)",
            "rhythm_pattern": "Four-on-floor kick, offbeat hi-hats, syncopated snare",
            "instruments": "Synth lead (81-87), Bass synth (38-39), Pad (88-95)",
            "characteristics": "Build-ups, drops, sidechain compression feel"
        },
        "hiphop": {
            "tempo_range": "80-100",
            "harmonic_progressions": "i-VI-III-VII (minor), i-iv-v (modal)",
            "rhythm_pattern": "Boom-bap (kick-snare), syncopated hi-hats, trap rolls",
            "instruments": "808 bass (38-39), Electric piano (4-5), Strings (48-51)",
            "characteristics": "Heavy bass, sample-like repetition"
        },
        "jazz": {
            "tempo_range": "100-140",
            "harmonic_progressions": "ii-V-I (Dm7-G7-Cmaj7), I-vi-ii-V turnaround, Use 7th chords",
            "rhythm_pattern": "Swing feel, walking bass quarter notes, ride cymbal",
            "instruments": "Piano (0-7), Upright bass (32-33), Brush drums",
            "characteristics": "Complex voicings, syncopation, improvisation"
        },
        "rock": {
            "tempo_range": "110-130",
            "harmonic_progressions": "I-IV-V (power chords), I-V-vi-IV, vi-IV-I-V",
            "rhythm_pattern": "Steady eighth notes, backbeat snare, crash on downbeats",
            "instruments": "Distorted guitar (29-31), Electric bass (33-34), Rock drums",
            "characteristics": "Power chords, driving rhythm, strong accents"
        },
        "ambient": {
            "tempo_range": "60-90",
            "harmonic_progressions": "Modal (static harmony), I-IV drone, Add9/sus2/sus4",
            "rhythm_pattern": "Minimal drums, long sustained notes",
            "instruments": "Pad (88-95), Strings (48-51), Bells/Chimes (8-15)",
            "characteristics": "Atmospheric, spacious, no clear downbeat"
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
            "harmonic_progressions": "I-IV-V-I (basic progression)",
            "rhythm_pattern": "Standard rhythm pattern",
            "instruments": "General MIDI instruments",
            "characteristics": "General music style"
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

        prompt = f"""Generate {bars}-bar {genre} music in JSON format.

**REQUIREMENTS:**
Genre: {genre} | Mood: {mood} | Tempo: {tempo_instruction} | Bars: {bars} ({max_quarter_notes} quarter notes in 4/4)

**HARMONIC PROGRESSION (CRITICAL):**
Style: {genre_info['harmonic_progressions']}
- Use ii-V-I progressions (Dm7→G7→Cmaj7 in C major) for sophistication
- Apply secondary dominants: V/V (D7→G7), V/vi (E7→Am) for variety
- Bass notes MUST outline chord roots and change every 2-4 bars
- Melody emphasizes chord tones (1, 3, 5, 7) with passing tones for movement

**RHYTHM & STYLE:**
Pattern: {genre_info['rhythm_pattern']}
Instruments: {genre_info['instruments']}
Character: {genre_info['characteristics']}
Mood: {mood_info}

**TRACKS (3-4 required):**
1. drums (program 0): {bars*8}+ notes. MIDI: 36=Kick 38=Snare 42=HH 49=Crash
2. bass (32-39): {bars*2}+ notes, outline chord roots
3. melody (0-7/24-31/80-87): {bars*4}+ notes, emphasize chord tones
4. chords (0-7/48-55): optional harmony

**COMPOSITION RULES:**
- Distribute notes evenly across 0-{max_quarter_notes} quarter notes (FULL {bars} bars)
- Change harmony every 2-4 bars for interest
- Align to rhythmic grid (quarter/eighth/sixteenth notes)
- Key: Choose appropriate key. Scale: major (uplifting) or minor (melancholic)
- Velocities: 0-127 for dynamics

**OUTPUT (JSON only, no text):**
{{"metadata":{{"tempo":<60-200>,"bars":{bars},"time_signature":[4,4],"key":"<C-B with #/b>","scale":"major/minor"}},
"tracks":[{{"name":"drums","instrument":"drums","midi_program":0,"notes":[{{"pitch":<0-127>,"start_time":<0-{max_quarter_notes}>,"duration":<float>,"velocity":<0-127>}}]}},{{"name":"bass","instrument":"<bass>","midi_program":<32-39>,"notes":[...]}},{{"name":"melody","instrument":"<instrument>","midi_program":<int>,"notes":[...]}}]}}

Generate musically coherent, genre-appropriate composition."""

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
