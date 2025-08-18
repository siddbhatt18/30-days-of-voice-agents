# services/streaming_stt.py
import asyncio
import json
import logging
import websockets
import base64
from fastapi import WebSocket
from config import ASSEMBLYAI_API_KEY

class StreamingTranscriber:
    """Handles real-time audio transcription using AssemblyAI's streaming API via WebSocket."""
    
    def __init__(self, websocket: WebSocket, sample_rate: int = 16000):
        self.websocket = websocket
        self.sample_rate = sample_rate
        self.assemblyai_ws = None
        self.running = False
        
        # Configure AssemblyAI
        if not ASSEMBLYAI_API_KEY:
            raise Exception("AssemblyAI API key not configured")
    
    async def start(self):
        """Start the streaming transcription session."""
        try:
            # Connect to AssemblyAI's WebSocket endpoint
            url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={self.sample_rate}"
            
            self.assemblyai_ws = await websockets.connect(
                url,
                extra_headers=[("Authorization", ASSEMBLYAI_API_KEY)],
                ping_interval=5,
                ping_timeout=20
            )
            
            self.running = True
            logging.info("Connected to AssemblyAI streaming service")
            
            # Start the receive loop
            asyncio.create_task(self._receive_loop())
            
        except Exception as e:
            logging.error(f"Failed to start streaming transcriber: {e}")
            raise
    
    async def send_audio(self, audio_data: bytes):
        """Send audio data to AssemblyAI for transcription."""
        if self.assemblyai_ws and self.running:
            try:
                # Convert audio bytes to base64
                audio_b64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Send audio data
                message = {"audio_data": audio_b64}
                await self.assemblyai_ws.send(json.dumps(message))
                
            except Exception as e:
                logging.error(f"Error sending audio data: {e}")
    
    async def close(self):
        """Close the streaming transcription session."""
        if self.assemblyai_ws and self.running:
            try:
                self.running = False
                
                # Send terminate message
                terminate_msg = {"terminate_session": True}
                await self.assemblyai_ws.send(json.dumps(terminate_msg))
                
                # Close WebSocket
                await self.assemblyai_ws.close()
                logging.info("Streaming transcriber closed")
                
            except Exception as e:
                logging.error(f"Error closing transcriber: {e}")
    
    async def _receive_loop(self):
        """Listen for transcription results from AssemblyAI."""
        try:
            async for message in self.assemblyai_ws:
                if not self.running:
                    break
                    
                try:
                    data = json.loads(message)
                    await self._handle_transcription_result(data)
                    
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing AssemblyAI message: {e}")
                    
        except Exception as e:
            logging.error(f"Error in receive loop: {e}")
    
    async def _handle_transcription_result(self, data: dict):
        """Handle transcription results from AssemblyAI."""
        try:
            # Check for different message types
            if data.get("message_type") == "SessionBegins":
                logging.info(f"AssemblyAI session started: {data.get('session_id')}")
                
            elif data.get("message_type") == "PartialTranscript":
                # Handle partial transcripts (optional - for real-time feedback)
                text = data.get("text", "").strip()
                if text:
                    logging.info(f"🎤 PARTIAL: {text}")
                    await self._send_to_client({
                        "type": "transcription",
                        "text": text,
                        "is_final": False
                    })
                    
            elif data.get("message_type") == "FinalTranscript":
                # Handle final transcripts
                text = data.get("text", "").strip()
                if text:
                    logging.info(f"🎤 TRANSCRIPTION: {text}")
                    await self._send_to_client({
                        "type": "transcription", 
                        "text": text,
                        "is_final": True
                    })
                    
            elif data.get("message_type") == "SessionTerminated":
                logging.info("AssemblyAI session terminated")
                self.running = False
                
            elif "error" in data:
                error_msg = data.get("error", "Unknown error")
                logging.error(f"AssemblyAI error: {error_msg}")
                await self._send_to_client({
                    "type": "error",
                    "message": error_msg
                })
                
        except Exception as e:
            logging.error(f"Error handling transcription result: {e}")
    
    async def _send_to_client(self, message: dict):
        """Send a message to the WebSocket client."""
        try:
            if self.websocket:
                await self.websocket.send_text(json.dumps(message))
        except Exception as e:
            logging.error(f"Failed to send message to client: {e}")