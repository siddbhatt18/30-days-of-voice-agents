# services/stt.py
import assemblyai as aai
from fastapi import UploadFile

def transcribe_audio(audio_file: UploadFile) -> str:
    """Transcribes audio to text using AssemblyAI."""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file.file)

    if transcript.status == aai.TranscriptStatus.error or not transcript.text:
        raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

    return transcript.text