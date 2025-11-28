"""
Quality Assurance Test Suite for BeatCanvas
Tests various scenarios and edge cases for the audio pipeline.
"""

import sys
import os
from app.models import MusicSchema, MetadataSchema, TrackSchema, NoteSchema
from app.services.midi_service import MidiService
from app.services.audio_service import AudioService

def test_scenario(name: str, music: MusicSchema, cleanup: bool = True):
    """Test a specific scenario."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")

    try:
        # Generate file paths
        midi_path = f"/tmp/test_{name.replace(' ', '_')}.mid"
        mp3_path = f"/tmp/test_{name.replace(' ', '_')}.mp3"

        # Services
        midi_service = MidiService()
        audio_service = AudioService()

        # Test pipeline
        print(f"📝 Metadata: {music.metadata.tempo} BPM, {music.metadata.bars} bars, {music.metadata.key} {music.metadata.scale}")
        print(f"🎹 Tracks: {len(music.tracks)}")

        # MIDI conversion
        print("  → Converting to MIDI...")
        midi_service.convert_json_to_midi(music, midi_path)
        print(f"  ✓ MIDI created ({os.path.getsize(midi_path)} bytes)")

        # Audio conversion
        print("  → Converting to MP3...")
        audio_service.midi_to_mp3(midi_path, mp3_path)
        mp3_size = os.path.getsize(mp3_path)
        print(f"  ✓ MP3 created ({mp3_size} bytes, {mp3_size / 1024:.1f} KB)")

        # Cleanup
        if cleanup:
            os.remove(midi_path)
            os.remove(mp3_path)
            print("  ✓ Cleaned up temporary files")

        print(f"✅ {name}: PASSED")
        return True

    except Exception as e:
        print(f"❌ {name}: FAILED - {str(e)}")
        return False


def main():
    results = []

    # Test 1: Minimum BPM (60) with 4 bars
    metadata_1 = MetadataSchema(
        tempo=60,
        bars=4,
        time_signature=[4, 4],
        key="C",
        scale="major"
    )
    kicks = [NoteSchema(pitch=36, start_time=float(i * 4), duration=0.25, velocity=100) for i in range(4)]
    music_1 = MusicSchema(
        metadata=metadata_1,
        tracks=[TrackSchema(name="drums", instrument="drums", midi_program=0, notes=kicks)]
    )
    results.append(test_scenario("Minimum BPM (60) - 4 bars", music_1))

    # Test 2: Maximum BPM (180) with 16 bars
    metadata_2 = MetadataSchema(
        tempo=180,
        bars=16,
        time_signature=[4, 4],
        key="A",
        scale="minor"
    )
    kicks = [NoteSchema(pitch=36, start_time=float(i * 4), duration=0.25, velocity=100) for i in range(16)]
    music_2 = MusicSchema(
        metadata=metadata_2,
        tracks=[TrackSchema(name="drums", instrument="drums", midi_program=0, notes=kicks)]
    )
    results.append(test_scenario("Maximum BPM (180) - 16 bars", music_2))

    # Test 3: Multiple instruments (drums + bass + melody)
    metadata_3 = MetadataSchema(
        tempo=120,
        bars=8,
        time_signature=[4, 4],
        key="G",
        scale="major"
    )

    # Drums
    drum_notes = [
        NoteSchema(pitch=36, start_time=float(i), duration=0.25, velocity=100)  # Kick every beat
        for i in range(0, 32, 1)
    ]
    drums = TrackSchema(name="drums", instrument="drums", midi_program=0, notes=drum_notes)

    # Bass (play root note pattern)
    bass_notes = [
        NoteSchema(pitch=43, start_time=float(i), duration=0.5, velocity=80)  # G2
        for i in range(0, 32, 2)
    ]
    bass = TrackSchema(name="bass", instrument="electric_bass", midi_program=33, notes=bass_notes)

    # Melody (simple ascending pattern)
    melody_notes = [
        NoteSchema(pitch=67 + (i % 8), start_time=float(i * 2), duration=1.0, velocity=70)  # G4-D5
        for i in range(16)
    ]
    melody = TrackSchema(name="lead", instrument="synth_lead", midi_program=80, notes=melody_notes)

    music_3 = MusicSchema(metadata=metadata_3, tracks=[drums, bass, melody])
    results.append(test_scenario("Multiple Instruments (Drums + Bass + Melody)", music_3))

    # Test 4: Edge case - Very low velocity
    metadata_4 = MetadataSchema(
        tempo=120,
        bars=4,
        time_signature=[4, 4],
        key="C",
        scale="major"
    )
    soft_notes = [
        NoteSchema(pitch=60, start_time=float(i), duration=0.5, velocity=10)
        for i in range(16)
    ]
    music_4 = MusicSchema(
        metadata=metadata_4,
        tracks=[TrackSchema(name="soft_piano", instrument="piano", midi_program=0, notes=soft_notes)]
    )
    results.append(test_scenario("Edge Case - Very Low Velocity (10)", music_4))

    # Test 5: Edge case - Very high pitch
    metadata_5 = MetadataSchema(
        tempo=120,
        bars=4,
        time_signature=[4, 4],
        key="C",
        scale="major"
    )
    high_notes = [
        NoteSchema(pitch=120, start_time=float(i), duration=0.5, velocity=80)
        for i in range(16)
    ]
    music_5 = MusicSchema(
        metadata=metadata_5,
        tracks=[TrackSchema(name="high_notes", instrument="flute", midi_program=73, notes=high_notes)]
    )
    results.append(test_scenario("Edge Case - Very High Pitch (120)", music_5))

    # Test 6: Standard BPM (128) with 8 bars (most common use case)
    metadata_6 = MetadataSchema(
        tempo=128,
        bars=8,
        time_signature=[4, 4],
        key="E",
        scale="minor"
    )
    standard_notes = [
        NoteSchema(pitch=36, start_time=float(i * 2), duration=0.25, velocity=100)
        for i in range(16)
    ]
    music_6 = MusicSchema(
        metadata=metadata_6,
        tracks=[TrackSchema(name="drums", instrument="drums", midi_program=0, notes=standard_notes)]
    )
    results.append(test_scenario("Standard Use Case (128 BPM - 8 bars)", music_6))

    # Summary
    print(f"\n{'='*60}")
    print("QA TEST SUMMARY")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    if passed == total:
        print("\n✅ ALL TESTS PASSED - System is ready for production!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED - Please review errors above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
