# services/tts.py
import requests
from typing import List, Dict, Any
from config import MURF_API_KEY # Import the key from config
from murf import Murf
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

MURF_API_URL = "https://api.murf.ai/v1/speech"

# Ensure uploads folder exists
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


def speak(text: str, output_file: str = "stream_output.wav"):
    """
    Convert text to speech using Murf API and save audio in uploads folder.
    """
    client = Murf(api_key=MURF_API_KEY)

    file_path = UPLOADS_DIR / output_file

    # Start with a clean file
    open(file_path, "wb").close()

    res = client.text_to_speech.stream(
        text=text,
        voice_id="en-US-ken",
        style="Conversational"
    )

    audio_bytes = b""
    for audio_chunk in res:
        audio_bytes += audio_chunk
        with open(file_path, "ab") as f:
            f.write(audio_chunk)

    return audio_bytes


def convert_text_to_speech(text: str, voice_id: str = "en-US-natalie") -> str:
    """Converts text to speech using Murf AI."""
    if not MURF_API_KEY:
        raise Exception("MURF_API_KEY not configured.")

    headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {
        "text": text,
        "voiceId": voice_id,
        "format": "MP3",
        "volume": "150%"
    }
    response = requests.post(f"{MURF_API_URL}/generate", json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data.get("audioFile")


def get_available_voices() -> List[Dict[str, Any]]:
    """Fetches the list of available voices from Murf AI."""
    if not MURF_API_KEY:
        raise Exception("MURF_API_KEY not configured.")

    headers = {"Accept": "application/json", "api-key": MURF_API_KEY}
    response = requests.get(f"{MURF_API_URL}/voices", headers=headers)
    response.raise_for_status()
    return response.json()