"""
Audio Service: Handles MIDI → WAV → MP3 conversion pipeline.
"""

import subprocess
import os
from pydub import AudioSegment
from app.config import settings


class AudioService:
    """Service for converting MIDI to audio formats (WAV and MP3)."""

    def midi_to_wav(self, midi_path: str, wav_path: str) -> None:
        """
        Converts MIDI file to WAV using fluidsynth.

        Args:
            midi_path: Path to input MIDI file
            wav_path: Path where WAV file should be saved

        Raises:
            RuntimeError: If fluidsynth conversion fails
            FileNotFoundError: If MIDI file or SoundFont not found
        """
        # Verify MIDI file exists
        if not os.path.exists(midi_path):
            raise FileNotFoundError(f"MIDI file not found: {midi_path}")

        # Verify SoundFont exists
        if not os.path.exists(settings.SOUNDFONT_PATH):
            raise FileNotFoundError(f"SoundFont file not found: {settings.SOUNDFONT_PATH}")

        # Build fluidsynth command (OPTIMIZED for speed)
        # Correct order: fluidsynth -ni -F output.wav -r 22050 soundfont.sf2 input.mid
        cmd = [
            "fluidsynth",
            "-ni",                          # Non-interactive mode
            "-F", wav_path,                 # Output WAV file
            "-r", "22050",                  # Sample rate (22.05kHz - 2x faster than 44.1kHz)
            "-o", "synth.reverb.active=no", # Disable reverb for speed
            "-o", "synth.chorus.active=no", # Disable chorus for speed
            "-g", "1.0",                    # Gain (1.0 = normal volume)
            settings.SOUNDFONT_PATH,        # SoundFont file
            midi_path                       # Input MIDI file
        ]

        # Run fluidsynth
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Fluidsynth conversion failed: {e.stderr}")

        # Verify WAV file was created
        if not os.path.exists(wav_path):
            raise RuntimeError("WAV file was not created")

    def wav_to_mp3(self, wav_path: str, mp3_path: str, bitrate: str = "192k") -> None:
        """
        Converts WAV file to MP3 using pydub (which uses ffmpeg).

        Args:
            wav_path: Path to input WAV file
            mp3_path: Path where MP3 file should be saved
            bitrate: MP3 bitrate (default: 192k)

        Raises:
            FileNotFoundError: If WAV file not found
            RuntimeError: If conversion fails
        """
        # Verify WAV file exists
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"WAV file not found: {wav_path}")

        try:
            # Load WAV file
            audio = AudioSegment.from_wav(wav_path)

            # Export as MP3
            audio.export(
                mp3_path,
                format="mp3",
                bitrate=bitrate,
                parameters=["-q:a", "2"]  # Quality setting (0-9, lower is better)
            )
        except Exception as e:
            raise RuntimeError(f"MP3 conversion failed: {str(e)}")

        # Verify MP3 file was created
        if not os.path.exists(mp3_path):
            raise RuntimeError("MP3 file was not created")

    def midi_to_mp3(self, midi_path: str, mp3_path: str, cleanup_wav: bool = True) -> None:
        """
        Converts MIDI directly to MP3 (via WAV intermediate).

        Args:
            midi_path: Path to input MIDI file
            mp3_path: Path where MP3 file should be saved
            cleanup_wav: Whether to delete intermediate WAV file (default: True)

        Raises:
            RuntimeError: If conversion fails
        """
        # Create temporary WAV path
        wav_path = mp3_path.replace(".mp3", ".wav")

        try:
            # MIDI → WAV
            self.midi_to_wav(midi_path, wav_path)

            # WAV → MP3
            self.wav_to_mp3(wav_path, mp3_path)

        finally:
            # Cleanup WAV file if requested
            if cleanup_wav and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except Exception:
                    pass  # Silent failure for cleanup


# Example usage for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        midi_file = sys.argv[1]
        service = AudioService()

        try:
            # Test MIDI → WAV
            wav_file = "/tmp/test.wav"
            print(f"Converting {midi_file} to WAV...")
            service.midi_to_wav(midi_file, wav_file)
            print(f"✓ WAV created: {wav_file}")

            # Test WAV → MP3
            mp3_file = "/tmp/test.mp3"
            print(f"Converting WAV to MP3...")
            service.wav_to_mp3(wav_file, mp3_file)
            print(f"✓ MP3 created: {mp3_file}")

            print("\nAudio conversion pipeline successful!")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python audio_service.py <midi_file>")
        sys.exit(1)
