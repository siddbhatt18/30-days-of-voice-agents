import asyncio
from typing import Callable, Optional, Type
from utils.logging_config import get_logger
import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    TerminationEvent,
    TurnEvent,
)

logger = get_logger(__name__)

class AssemblyAIStreamingService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client: Optional[StreamingClient] = None
        self.is_streaming = False
        self.transcription_callback: Optional[Callable] = None
        self.websocket_callback: Optional[Callable] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._active = False
        
    def set_transcription_callback(self, callback: Callable):
        self.transcription_callback = callback
        
    def is_active(self):
        return self._active and self.is_streaming
        
    def on_begin(self, client: Type[StreamingClient], event: BeginEvent):
        self._active = True
        if self.websocket_callback and self.loop:
            try:
                coro = self.websocket_callback({
                    "type": "transcription_session_started",
                    "message": "Transcription session started",
                    "session_id": event.id
                })
                if coro is not None:
                    asyncio.run_coroutine_threadsafe(coro, self.loop)
            except Exception as cb_error:
                logger.error(f"Error in begin callback: {cb_error}")
    
    def on_turn(self, client: Type[StreamingClient], event: TurnEvent):
        try:
            # Always process the transcription, even if empty, to handle turn detection
            if self.transcription_callback and self.loop:
                transcript_data = {
                    "type": "final_transcript" if event.end_of_turn else "partial_transcript",
                    "text": event.transcript,
                    "confidence": getattr(event, 'end_of_turn_confidence', None),
                    "is_final": event.end_of_turn,
                    "turn_order": getattr(event, 'turn_order', None),
                    "turn_is_formatted": getattr(event, 'turn_is_formatted', False),
                    "end_of_turn": event.end_of_turn
                }
                try:
                    coro = self.transcription_callback(transcript_data)
                    if coro is not None:
                        asyncio.run_coroutine_threadsafe(coro, self.loop)
                except Exception as cb_error:
                    logger.error(f"Error in transcription callback: {cb_error}")
            
            # Send a separate turn end notification when the user stops talking
            if event.end_of_turn and self.websocket_callback and self.loop:
                try:
                    turn_end_data = {
                        "type": "turn_end",
                        "message": "User has stopped talking",
                        "final_transcript": event.transcript,
                        "confidence": getattr(event, 'end_of_turn_confidence', None),
                        "turn_order": getattr(event, 'turn_order', None),
                        "turn_is_formatted": getattr(event, 'turn_is_formatted', False)
                    }
                    coro = self.websocket_callback(turn_end_data)
                    if coro is not None:
                        asyncio.run_coroutine_threadsafe(coro, self.loop)
                except Exception as cb_error:
                    logger.error(f"Error in turn end callback: {cb_error}")
                
        except Exception as e:
            logger.error(f"Error processing turn event: {e}")
    
    def on_terminated(self, client: Type[StreamingClient], event: TerminationEvent):
        self._active = False
        if self.websocket_callback and self.loop:
            try:
                coro = self.websocket_callback({
                    "type": "transcription_session_terminated",
                    "message": "Transcription session ended",
                    "audio_duration": event.audio_duration_seconds
                })
                if coro is not None:
                    asyncio.run_coroutine_threadsafe(coro, self.loop)
            except Exception as cb_error:
                logger.error(f"Error in termination callback: {cb_error}")
    
    def on_error(self, client: Type[StreamingClient], error: StreamingError):
        logger.error(f"AssemblyAI streaming error: {error}")
        self._active = False
        if self.transcription_callback and self.loop:
            try:
                coro = self.transcription_callback({
                    "type": "transcription_error",
                    "message": str(error),
                    "status": "error"
                })
                if coro is not None:
                    asyncio.run_coroutine_threadsafe(coro, self.loop)
            except Exception as cb_error:
                logger.error(f"Error in error callback: {cb_error}")
        
    async def start_streaming_transcription(self, websocket_callback=None):
        try:
            self.websocket_callback = websocket_callback
            self.is_streaming = True
            self.loop = asyncio.get_running_loop()
            self.client = StreamingClient(
                StreamingClientOptions(
                    api_key=self.api_key,
                    api_host="streaming.assemblyai.com",
                )
            )
            self.client.on(StreamingEvents.Begin, self.on_begin)
            self.client.on(StreamingEvents.Turn, self.on_turn)
            self.client.on(StreamingEvents.Termination, self.on_terminated)
            self.client.on(StreamingEvents.Error, self.on_error)

            self.client.connect(
                StreamingParameters(
                    sample_rate=16000,
                    encoding='pcm_s16le',  # 16-bit signed little-endian PCM
                    format_turns=True,     # Enable text formatting
                    end_of_turn_confidence_threshold=0.5,  # Lower threshold for faster detection
                    min_end_of_turn_silence_when_confident=300,  # 300ms for better detection
                )
            )
            
            logger.info("Connected to AssemblyAI Universal Streaming")
            
            if websocket_callback:
                await websocket_callback({
                    "type": "transcription_ready",
                    "message": "AssemblyAI Universal Streaming connected and ready",
                    "status": "ready"
                })
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to start AssemblyAI Universal Streaming: {e}")
            self.is_streaming = False
            self._active = False
            if websocket_callback:
                await websocket_callback({
                    "type": "transcription_error", 
                    "message": f"Failed to start transcription: {str(e)}",
                    "status": "error"
                })
            return False
    
    async def send_audio_chunk(self, audio_data: bytes):
        try:
            if self.client and self.is_streaming and self._active:
                logger.debug(f"Sending {len(audio_data)} bytes to AssemblyAI Universal Streaming")
                if len(audio_data) > 0:
                    self.client.stream(audio_data)
                    logger.debug(f"Successfully sent {len(audio_data)} bytes to AssemblyAI")
                else:
                    logger.warning("Empty audio chunk received")
                return True
            else:
                logger.warning(f"Streaming client not ready (active: {self._active}, streaming: {self.is_streaming})")
                return False
                
        except Exception as e:
            logger.error(f"Error sending audio to AssemblyAI Universal Streaming: {e}")
            return False
    
    async def stop_streaming_transcription(self, websocket_callback=None):
        try:
            self.is_streaming = False
            self._active = False
            
            if self.client:
                self.client.disconnect(terminate=True)
                self.client = None
            self.loop = None
                
            logger.info("AssemblyAI Universal Streaming transcription stopped")
            
            if websocket_callback:
                await websocket_callback({
                    "type": "transcription_stopped",
                    "message": "Universal Streaming transcription service stopped",
                    "status": "stopped"
                })
                
        except Exception as e:
            logger.error(f"Error stopping AssemblyAI Universal Streaming: {e}")
            if websocket_callback:
                await websocket_callback({
                    "type": "transcription_error",
                    "message": f"Error stopping transcription: {str(e)}",
                    "status": "error"
                })
