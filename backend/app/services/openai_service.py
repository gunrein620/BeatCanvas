"""
OpenAI Service: Handles communication with OpenAI API for music generation.
"""

import json
from typing import Optional
from openai import OpenAI
from app.config import settings
from app.models import MusicSchema
from app.utils.prompt_builder import PromptBuilder


class OpenAIService:
    """Service for generating music JSON using OpenAI GPT-4 Turbo."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_builder = PromptBuilder()

    def _extend_music_pattern(self, music_schema: MusicSchema, current_length: float, target_length: float) -> MusicSchema:
        """
        Extend music by repeating the pattern until target length is reached.
        Each track is extended independently based on its own pattern length.

        Args:
            music_schema: Original music schema
            current_length: Current max length in quarter notes (not used, kept for compatibility)
            target_length: Target length in quarter notes

        Returns:
            Extended music schema
        """
        from app.models import NoteSchema, TrackSchema

        # Extend each track independently
        extended_tracks = []
        for track in music_schema.tracks:
            # Calculate this track's actual pattern length
            track_max_time = 0.0
            for note in track.notes:
                note_end = note.start_time + note.duration
                if note_end > track_max_time:
                    track_max_time = note_end

            if track_max_time <= 0:
                # Track has no notes, skip
                extended_tracks.append(track)
                continue

            # Round to nearest bar (4 quarter notes) for clean looping
            pattern_length = round(track_max_time / 4) * 4
            if pattern_length == 0:
                pattern_length = 4  # At least 1 bar

            print(f"  Track '{track.name}': pattern_length={pattern_length} quarter notes, target={target_length}")

            # Calculate how many repetitions needed
            repetitions_needed = int(target_length / pattern_length) + 1

            extended_notes = []

            # Copy and repeat notes
            for rep in range(repetitions_needed):
                offset = pattern_length * rep
                for note in track.notes:
                    new_start = note.start_time + offset
                    new_end = new_start + note.duration

                    # Only add if within target length
                    if new_start < target_length:
                        # Clip duration if it exceeds target
                        if new_end > target_length:
                            clipped_duration = target_length - new_start
                            if clipped_duration > 0:
                                extended_notes.append(
                                    NoteSchema(
                                        pitch=note.pitch,
                                        start_time=new_start,
                                        duration=clipped_duration,
                                        velocity=note.velocity
                                    )
                                )
                        else:
                            extended_notes.append(
                                NoteSchema(
                                    pitch=note.pitch,
                                    start_time=new_start,
                                    duration=note.duration,
                                    velocity=note.velocity
                                )
                            )

            # Create extended track
            extended_tracks.append(
                TrackSchema(
                    name=track.name,
                    instrument=track.instrument,
                    midi_program=track.midi_program,
                    notes=extended_notes
                )
            )

            print(f"    → Extended from {len(track.notes)} to {len(extended_notes)} notes")

        # Update music schema with extended tracks
        music_schema.tracks = extended_tracks
        return music_schema

    async def generate_music_json(
        self,
        genre: str,
        mood: str,
        tempo: Optional[int] = None,
        bars: int = 8
    ) -> MusicSchema:
        """
        Generate music JSON using OpenAI GPT-4 Turbo.

        Args:
            genre: Music genre (e.g., EDM, Jazz, Hip-Hop)
            mood: Music mood (e.g., Happy, Sad, Energetic)
            tempo: Optional specific tempo (BPM)
            bars: Number of bars (4, 8, or 16)

        Returns:
            MusicSchema object containing the generated composition

        Raises:
            ValueError: If OpenAI returns invalid JSON
            Exception: If OpenAI API call fails
        """
        # Build the prompt
        prompt = self.prompt_builder.build_music_generation_prompt(
            genre=genre,
            mood=mood,
            tempo=tempo,
            bars=bars
        )

        try:
            # Call OpenAI API with JSON mode
            # Calculate max_tokens based on bars (more bars = more notes = more tokens needed)
            # gpt-4-turbo-preview supports max 4096 completion tokens
            max_tokens = min(3000 + (bars * 100), 4096)  # Scale with bars, cap at 4096

            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # GPT-4 Turbo
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional music composer AI that generates music compositions in JSON format. You output ONLY valid JSON with no additional text, comments, or explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},  # Enforce JSON output
                temperature=0.8,  # Creative but not too random
                max_tokens=max_tokens
            )

            # Extract JSON from response
            json_str = response.choices[0].message.content

            if not json_str:
                raise ValueError("OpenAI returned empty response")

            # Parse JSON
            try:
                music_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"\n!!! JSON PARSE ERROR !!!")
                print(f"Error: {e}")
                print(f"Response content (first 1000 chars):")
                print(json_str[:1000])
                print(f"\nResponse content (around error position):")
                start = max(0, e.pos - 100)
                end = min(len(json_str), e.pos + 100)
                print(json_str[start:end])
                print(f"\n!!!!!!!!!!!!!!!!!!!!!")
                raise

            # Validate against Pydantic schema
            music_schema = MusicSchema(**music_data)

            # Validate that music actually spans the requested bars
            expected_quarter_notes = bars * 4

            # Check each track's length and note count
            print(f"\n=== VALIDATING TRACK LENGTHS ===")
            needs_extension = False

            # Expected minimum notes per track
            expected_notes = {
                'drums': bars * 8,   # At least 8 notes per bar
                'bass': bars * 2,    # At least 2 notes per bar
                'melody': bars * 4,  # At least 4 notes per bar
            }

            for track in music_schema.tracks:
                track_max = 0.0
                for note in track.notes:
                    note_end = note.start_time + note.duration
                    if note_end > track_max:
                        track_max = note_end

                note_count = len(track.notes)
                track_name_lower = track.name.lower()
                expected = expected_notes.get(track_name_lower, bars * 2)

                status = "✓" if note_count >= expected else "✗ TOO FEW"
                print(f"  {track.name}: {note_count} notes (expected ≥{expected}) {status}, length: {track_max:.2f} quarter notes ({track_max/4:.2f} bars)")

                # If any track is less than 75% of expected, needs extension
                if track_max < expected_quarter_notes * 0.75:
                    needs_extension = True

            # Auto-extend if any track is too short
            if needs_extension:
                print(f"\nWARNING: Some tracks are too short!")
                print(f"  Requested: {bars} bars ({expected_quarter_notes} quarter notes)")
                print(f"  Auto-extending by repeating patterns...\n")

                # Extend the music by repeating the pattern
                music_schema = self._extend_music_pattern(music_schema, 0, expected_quarter_notes)

                # Verify extension worked
                print(f"\n=== VERIFICATION AFTER EXTENSION ===")
                for track in music_schema.tracks:
                    track_max = 0.0
                    for note in track.notes:
                        note_end = note.start_time + note.duration
                        if note_end > track_max:
                            track_max = note_end
                    print(f"  {track.name}: {track_max:.2f} quarter notes ({track_max/4:.2f} bars)")
                print(f"=================================\n")

            return music_schema

        except json.JSONDecodeError as e:
            raise ValueError(f"OpenAI returned invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


# Example usage for testing
if __name__ == "__main__":
    import asyncio

    async def test_generation():
        """Test music generation."""
        service = OpenAIService()

        print("Generating music with GPT-4 Turbo...")
        print("Genre: EDM, Mood: Energetic, Tempo: 128 BPM, Bars: 4\n")

        try:
            music = await service.generate_music_json(
                genre="EDM",
                mood="Energetic",
                tempo=128,
                bars=4
            )

            print("✓ Music generated successfully!")
            print(f"\nMetadata:")
            print(f"  Tempo: {music.metadata.tempo} BPM")
            print(f"  Bars: {music.metadata.bars}")
            print(f"  Key: {music.metadata.key} {music.metadata.scale}")
            print(f"  Time signature: {music.metadata.time_signature[0]}/{music.metadata.time_signature[1]}")

            print(f"\nTracks ({len(music.tracks)}):")
            for track in music.tracks:
                print(f"  - {track.name}: {len(track.notes)} notes (program {track.midi_program})")

            # Save to file for inspection
            with open("/tmp/generated_music.json", "w") as f:
                json.dump(music.model_dump(), f, indent=2)
            print(f"\n✓ Full JSON saved to /tmp/generated_music.json")

        except Exception as e:
            print(f"✗ Error: {e}")

    # Run the test
    asyncio.run(test_generation())
