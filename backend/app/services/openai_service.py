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
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # GPT-4 Turbo
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional music composer AI that generates music compositions in JSON format. You output only valid JSON, nothing else."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},  # Enforce JSON output
                temperature=0.8,  # Creative but not too random
                max_tokens=4000   # Enough for complex compositions
            )

            # Extract JSON from response
            json_str = response.choices[0].message.content

            if not json_str:
                raise ValueError("OpenAI returned empty response")

            # Parse JSON
            music_data = json.loads(json_str)

            # Validate against Pydantic schema
            music_schema = MusicSchema(**music_data)

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
