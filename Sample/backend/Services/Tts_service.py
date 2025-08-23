import os
import logging
from murf import Murf
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

logger = logging.getLogger(__name__)
MURF_API_KEY = os.getenv("MURF_API_KEY")

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
