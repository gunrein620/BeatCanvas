"""
MIDI Service: Converts music JSON to MIDI files using pretty_midi.
"""

import pretty_midi
from app.models import MusicSchema


class MidiService:
    """Service for converting music JSON to MIDI files."""

    def convert_json_to_midi(self, music_data: MusicSchema, output_path: str) -> None:
        """
        Converts music JSON schema to a MIDI file.

        Args:
            music_data: MusicSchema object containing the composition
            output_path: Path where the MIDI file should be saved

        Raises:
            ValueError: If music data is invalid
            IOError: If file cannot be written
        """
        # Create MIDI object with the specified tempo
        midi = pretty_midi.PrettyMIDI(initial_tempo=float(music_data.metadata.tempo))

        # Calculate seconds per beat based on tempo
        tempo = music_data.metadata.tempo
        seconds_per_beat = 60.0 / tempo

        # Process each track
        for track in music_data.tracks:
            # Create instrument
            # Drums use channel 10 (is_drum=True), others are melodic
            is_drum_track = track.instrument.lower() == "drums"
            instrument = pretty_midi.Instrument(
                program=track.midi_program,
                is_drum=is_drum_track,
                name=track.name
            )

            # Add notes to the instrument
            for note_data in track.notes:
                # Convert timing from quarter notes to seconds
                start_time_sec = note_data.start_time * seconds_per_beat
                end_time_sec = (note_data.start_time + note_data.duration) * seconds_per_beat

                # Create MIDI note
                midi_note = pretty_midi.Note(
                    velocity=note_data.velocity,
                    pitch=note_data.pitch,
                    start=start_time_sec,
                    end=end_time_sec
                )

                instrument.notes.append(midi_note)

            # Add instrument to MIDI
            midi.instruments.append(instrument)

        # Write MIDI file
        midi.write(output_path)


# Example usage for testing
if __name__ == "__main__":
    from app.models import MetadataSchema, TrackSchema, NoteSchema

    # Create sample music data (simple kick drum pattern)
    metadata = MetadataSchema(
        tempo=120,
        bars=4,
        time_signature=[4, 4],
        key="C",
        scale="major"
    )

    # Create a simple kick drum pattern (4 kicks over 4 bars)
    kicks = [
        NoteSchema(pitch=36, start_time=float(i * 4), duration=0.25, velocity=100)
        for i in range(4)
    ]

    drums_track = TrackSchema(
        name="drums",
        instrument="drums",
        midi_program=0,
        notes=kicks
    )

    music = MusicSchema(metadata=metadata, tracks=[drums_track])

    # Test conversion
    service = MidiService()
    service.convert_json_to_midi(music, "/tmp/test.mid")
    print("✓ Test MIDI file created at /tmp/test.mid")
