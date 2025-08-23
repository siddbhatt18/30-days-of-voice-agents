from murf import Murf
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TTSService:
    def __init__(self, api_key: str, voice_id: str = "en-IN-aarav"):
        self.api_key = api_key
        self.voice_id = voice_id
        self.client = Murf(api_key=api_key)
    
    def truncate_text_for_murf(self, text: str, max_chars: int = 3000) -> str:
        if len(text) <= max_chars:
            return text
            
        truncated = text[:max_chars]
        last_sentence_end = max(
            truncated.rfind('.'),
            truncated.rfind('!'),
            truncated.rfind('?')
        )
        
        if last_sentence_end > max_chars * 0.7:
            return truncated[:last_sentence_end + 1]
        else:
            last_space = truncated.rfind(' ')
            if last_space > 0:
                return truncated[:last_space] + "..."
            else:
                return truncated + "..."
    
    async def generate_speech(self, text: str, format: str = "MP3") -> Optional[str]:
        try:
            murf_text = self.truncate_text_for_murf(text)
            
            murf_response = self.client.text_to_speech.generate(
                text=murf_text,
                voice_id=self.voice_id,
                format=format
            )
            
            audio_url = murf_response.audio_file
            
            if not audio_url:
                raise Exception("No audio URL returned from Murf API")
                
            logger.info("TTS audio generated successfully")
            return audio_url
            
        except Exception as e:
            logger.error(f"TTS generation error: {str(e)}")
            raise
    
    async def generate_fallback_audio(self, error_message: str) -> Optional[str]:
        try:
            return await self.generate_speech(error_message)
        except Exception as e:
            logger.error(f"Failed to generate fallback audio: {str(e)}")
            return None
