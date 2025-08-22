# services/tts.py
import requests
from typing import List, Dict, Any
from config import MURF_API_KEY # Import the key from config

MURF_API_URL = "https://api.murf.ai/v1/speech"

def convert_text_to_speech(text: str, voice_id: str = "en-US-natalie") -> str:
    """Converts text to speech using Murf AI."""
    if not MURF_API_KEY:
        raise Exception("MURF_API_KEY not configured.")

    headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {
        "text": text,
        "voiceId": voice_id,
        "format": "MP3",
        "volume": "100%"
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