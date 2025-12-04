"""
API endpoints for BeatCanvas music generation.
"""

import os
import uuid
import time
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.models import GenerateRequest
from app.services.openai_service import OpenAIService
from app.services.midi_service import MidiService
from app.services.audio_service import AudioService
from app.config import settings


router = APIRouter()


@router.post("/generate")
async def generate_music(
    request: GenerateRequest,
    background_tasks: BackgroundTasks
) -> FileResponse:
    """
    Generate music from genre/mood input.

    Flow:
    1. Validate input (Pydantic)
    2. Generate music JSON with OpenAI
    3. Convert JSON → MIDI
    4. Convert MIDI → WAV
    5. Convert WAV → MP3
    6. Return MP3 file
    7. Cleanup temp files in background

    Args:
        request: GenerateRequest with genre, mood, tempo (optional), bars
        background_tasks: FastAPI background tasks for cleanup

    Returns:
        FileResponse with MP3 audio file

    Raises:
        HTTPException: On any error during generation
    """
    # Generate unique ID for this request
    request_id = str(uuid.uuid4())

    # Ensure temp directory exists
    os.makedirs(settings.TEMP_DIR, exist_ok=True)

    # Define file paths
    midi_path = os.path.join(settings.TEMP_DIR, f"{request_id}.mid")
    wav_path = os.path.join(settings.TEMP_DIR, f"{request_id}.wav")
    mp3_path = os.path.join(settings.TEMP_DIR, f"{request_id}.mp3")

    try:
        total_start = time.time()

        # Step 1: Generate music JSON with OpenAI
        print(f"\n=== GENERATE REQUEST ===")
        print(f"Genre: {request.genre}")
        print(f"Mood: {request.mood}")
        print(f"Tempo: {request.tempo}")
        print(f"Bars: {request.bars}")
        print(f"========================\n")

        step1_start = time.time()
        openai_service = OpenAIService()
        music_data = await openai_service.generate_music_json(
            genre=request.genre,
            mood=request.mood,
            tempo=request.tempo,
            bars=request.bars
        )
        step1_time = time.time() - step1_start

        print(f"\n=== GENERATED MUSIC DATA ===")
        print(f"Tempo: {music_data.metadata.tempo}")
        print(f"Bars: {music_data.metadata.bars}")
        print(f"Key: {music_data.metadata.key} {music_data.metadata.scale}")
        print(f"Tracks: {len(music_data.tracks)}")
        for track in music_data.tracks:
            max_time = max((note.start_time + note.duration for note in track.notes), default=0)
            print(f"  - {track.name}: {len(track.notes)} notes, max_time: {max_time:.2f} quarter notes")
        print(f"============================\n")

        # Step 2: JSON → MIDI
        step2_start = time.time()
        midi_service = MidiService()
        midi_service.convert_json_to_midi(music_data, midi_path)
        step2_time = time.time() - step2_start

        # Step 3: MIDI → WAV
        step3_start = time.time()
        audio_service = AudioService()
        audio_service.midi_to_wav(midi_path, wav_path)
        step3_time = time.time() - step3_start

        # Step 4: WAV → MP3
        step4_start = time.time()
        audio_service.wav_to_mp3(wav_path, mp3_path)
        step4_time = time.time() - step4_start

        total_time = time.time() - total_start

        # Print timing breakdown
        print(f"\n=== PERFORMANCE BREAKDOWN ===")
        print(f"Step 1 (OpenAI API):  {step1_time:.2f}s ({step1_time/total_time*100:.1f}%)")
        print(f"Step 2 (JSON→MIDI):   {step2_time:.2f}s ({step2_time/total_time*100:.1f}%)")
        print(f"Step 3 (MIDI→WAV):    {step3_time:.2f}s ({step3_time/total_time*100:.1f}%) ← BOTTLENECK?")
        print(f"Step 4 (WAV→MP3):     {step4_time:.2f}s ({step4_time/total_time*100:.1f}%)")
        print(f"TOTAL TIME:           {total_time:.2f}s")
        print(f"============================\n")

        # Step 5: Schedule cleanup in background
        def cleanup():
            """Delete temporary files after response is sent."""
            for path in [midi_path, wav_path, mp3_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass  # Silent failure for cleanup

        background_tasks.add_task(cleanup)

        # Step 6: Return MP3 file
        filename = f"beatcanvas_{request.genre}_{request.mood}_{request.bars}bars.mp3"
        return FileResponse(
            path=mp3_path,
            media_type="audio/mpeg",
            filename=filename,
            headers={
                "X-Tempo": str(music_data.metadata.tempo),
                "X-Bars": str(music_data.metadata.bars),
                "X-Key": music_data.metadata.key,
                "X-Scale": music_data.metadata.scale
            }
        )

    except Exception as e:
        # Cleanup on error
        for path in [midi_path, wav_path, mp3_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

        # Determine appropriate error code
        error_message = str(e)
        if "OpenAI" in error_message or "API" in error_message:
            status_code = 503  # Service Unavailable
        elif "SoundFont" in error_message or "fluidsynth" in error_message:
            status_code = 500  # Internal Server Error
        else:
            status_code = 500

        raise HTTPException(
            status_code=status_code,
            detail=f"Music generation failed: {error_message}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status information
    """
    return {
        "status": "healthy",
        "service": "BeatCanvas API",
        "version": "1.0.0"
    }
