import assemblyai as aai
import tempfile
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class STTService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        aai.settings.api_key = api_key
        self.transcriber = aai.Transcriber()
    
    async def transcribe_audio(self, audio_content: bytes) -> Optional[str]:
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_content)
                tmp_path = tmp.name
            
            transcript = self.transcriber.transcribe(tmp_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                raise Exception(f"AssemblyAI transcription error: {transcript.error}")
            
            if not transcript.text or transcript.text.strip() == "":
                logger.warning("No speech detected in audio")
                return None
            
            transcribed_text = transcript.text.strip()
            logger.info(f"Successfully transcribed: {transcribed_text[:100]}...")
            return transcribed_text
            
        except Exception as e:
            logger.error(f"STT transcription error: {str(e)}")
            raise
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    logger.warning(f"Failed to delete temporary file: {tmp_path}")
