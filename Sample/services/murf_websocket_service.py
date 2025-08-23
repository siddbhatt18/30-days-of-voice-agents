import asyncio
import websockets
import json
import base64
import uuid
from typing import Optional, AsyncGenerator
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class MurfWebSocketService:
    """Murf WebSocket TTS service for streaming text-to-speech"""
    
    def __init__(self, api_key: str, voice_id: str = "en-US-amara"):
        self.api_key = api_key
        self.voice_id = voice_id
        self.ws_url = "wss://api.murf.ai/v1/speech/stream-input"
        self.websocket = None
        self.is_connected = False
        # Use a static context_id as requested to avoid context limit exceeded errors
        self.static_context_id = "voice_agent_context_static"
        # Add a lock to prevent concurrent recv() calls
        self._recv_lock = asyncio.Lock()
        self._connecting = False
        
    async def connect(self):
        """Establish WebSocket connection to Murf"""
        # Prevent multiple concurrent connections
        if self._connecting or self.is_connected:
            logger.info("Already connected or connecting to Murf WebSocket")
            return
            
        self._connecting = True
        try:
            connection_url = f"{self.ws_url}?api-key={self.api_key}&sample_rate=44100&channel_type=MONO&format=WAV"
            self.websocket = await websockets.connect(connection_url)
            self.is_connected = True
            logger.info("✅ Connected to Murf WebSocket")
            
            # Clear any existing context first to avoid "Exceeded Active context limit"
            await self.clear_context()
            
            # Send initial voice configuration
            await self._send_voice_config()
            
        except Exception as e:
            logger.error(f"Failed to connect to Murf WebSocket: {str(e)}")
            self.is_connected = False
            raise
        finally:
            self._connecting = False
    
    async def _send_voice_config(self):
        """Send voice configuration to Murf WebSocket"""
        try:
            voice_config_msg = {
                "voice_config": {
                    "voiceId": self.voice_id,
                    "style": "Conversational",
                    "rate": 0,
                    "pitch": 0,
                    "variation": 1
                },
                "context_id": self.static_context_id
            }
            logger.info(f"Sending voice config: {voice_config_msg}")
            await self.websocket.send(json.dumps(voice_config_msg))
            
            # Wait for voice config acknowledgment with recv lock
            async with self._recv_lock:
                try:
                    response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    logger.info(f"Voice config response: {data}")
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for voice config acknowledgment")
            
        except Exception as e:
            logger.error(f"Failed to send voice config: {str(e)}")
            raise
    
    async def disconnect(self):
        """Close WebSocket connection"""
        try:
            if self.websocket and self.is_connected:
                await self.websocket.close()
                self.is_connected = False
                logger.info("Disconnected from Murf WebSocket")
        except Exception as e:
            logger.error(f"Error disconnecting from Murf WebSocket: {str(e)}")
    
    async def stream_text_to_audio(self, text_stream: AsyncGenerator[str, None]) -> AsyncGenerator[dict, None]:
        """
        Stream text chunks to Murf and yield base64 audio responses
        
        Args:
            text_stream: Async generator of text chunks from LLM
            
        Yields:
            dict: Response containing base64 audio data and metadata
        """
        if not self.is_connected:
            raise Exception("WebSocket not connected. Call connect() first.")
        
        try:
            accumulated_text = ""
            chunk_count = 0
            
            # Collect all text chunks first
            text_chunks = []
            async for text_chunk in text_stream:
                if text_chunk:
                    text_chunks.append(text_chunk)
                    accumulated_text += text_chunk
                    chunk_count += 1
            
            logger.info(f"Collected {chunk_count} text chunks, total length: {len(accumulated_text)}")
            
            # Send all text in one message (better for TTS quality)
            text_msg = {
                "context_id": self.static_context_id,
                "text": accumulated_text,
                "end": True  # Close context immediately for better audio quality
            }
            
            logger.info(f"Sending complete text ({len(accumulated_text)} chars): {accumulated_text[:100]}...")
            await self.websocket.send(json.dumps(text_msg))
            
            # Now listen for audio responses
            async for audio_response in self._listen_for_audio():
                yield audio_response
                # Break on final audio chunk
                if audio_response.get("type") == "audio_chunk" and audio_response.get("is_final"):
                    break
            
        except Exception as e:
            logger.error(f"Error in stream_text_to_audio: {str(e)}")
            raise
    
    async def _listen_for_audio(self) -> AsyncGenerator[dict, None]:
        """Listen for audio responses from Murf WebSocket"""
        audio_chunk_count = 0
        total_audio_size = 0
        
        try:
            while True:
                try:
                    # Use recv lock to prevent concurrent recv() calls
                    async with self._recv_lock:
                        response = await asyncio.wait_for(self.websocket.recv(), timeout=30.0)
                    
                    data = json.loads(response)
                    logger.info(f"📥 Received response: {list(data.keys())}")
                    
                    if "audio" in data:
                        audio_chunk_count += 1
                        audio_base64 = data["audio"]
                        total_audio_size += len(audio_base64)
                        
                        # Print base64 audio to console as requested
                        print(f"\n🎵 === MURF BASE64 AUDIO CHUNK {audio_chunk_count} ===")
                        print(f"Context ID: {data.get('context_id', 'N/A')}")
                        print(f"Base64 Audio Size: {len(audio_base64)} characters")
                        print(f"Base64 Audio Preview: {audio_base64[:100]}...")
                        # print(f"Base64 Audio (Full): {audio_base64}")
                        print(f"Final: {data.get('final', False)}")
                        print(f"=== END AUDIO CHUNK {audio_chunk_count} ===\n")
                        
                        # Yield the response
                        yield {
                            "type": "audio_chunk",
                            "audio_base64": audio_base64,
                            "context_id": data.get("context_id"),
                            "chunk_number": audio_chunk_count,
                            "chunk_size": len(audio_base64),
                            "total_size": total_audio_size,
                            "timestamp": datetime.now().isoformat(),
                            "is_final": data.get("final", False)
                        }
                        
                        # Check if this is the final audio chunk
                        if data.get("final"):
                            logger.info(f"Received final audio chunk. Total chunks: {audio_chunk_count}, Total size: {total_audio_size}")
                            break
                    
                    else:
                        # Non-audio response
                        print(f"📊 Non-audio response: {data}")
                        logger.info(f"Received non-audio response: {data}")
                        yield {
                            "type": "status",
                            "data": data,
                            "timestamp": datetime.now().isoformat()
                        }
                
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for Murf response")
                    break
                except websockets.exceptions.ConnectionClosed:
                    logger.info("Murf WebSocket connection closed")
                    break
                except Exception as e:
                    logger.error(f"Error receiving from Murf WebSocket: {str(e)}")
                    break
            
        except Exception as e:
            logger.error(f"Error in _listen_for_audio (total chunks processed: {audio_chunk_count}): {str(e)}")
            raise
    
    async def send_single_text(self, text: str) -> AsyncGenerator[dict, None]:
        """
        Send a single text message to Murf and receive audio response
        
        Args:
            text: Complete text to convert to speech
            
        Yields:
            dict: Response containing base64 audio data and metadata
        """
        if not self.is_connected:
            raise Exception("WebSocket not connected. Call connect() first.")
        
        try:
            # Send complete text in one message
            text_msg = {
                "context_id": self.static_context_id,
                "text": text,
                "end": True  # Close context immediately
            }
            
            logger.info(f"Sending complete text: {text[:100]}...")
            await self.websocket.send(json.dumps(text_msg))
            
            # Listen for audio responses
            async for audio_response in self._listen_for_audio():
                yield audio_response
                
        except Exception as e:
            logger.error(f"Error in send_single_text: {str(e)}")
            raise
    
    async def clear_context(self):
        """Clear the current context to handle interruptions"""
        try:
            if not self.websocket or not self.is_connected:
                return  # No connection to clear
                
            clear_msg = {
                "context_id": self.static_context_id,
                "clear": True
            }
            
            logger.info("Clearing Murf context to avoid context limit errors")
            await self.websocket.send(json.dumps(clear_msg))
            
            # Use the recv lock to prevent concurrency issues
            async with self._recv_lock:
                try:
                    response = await asyncio.wait_for(self.websocket.recv(), timeout=3.0)
                    data = json.loads(response)
                    logger.info(f"Context clear response: {data}")
                except asyncio.TimeoutError:
                    logger.warning("Timeout waiting for context clear acknowledgment")
            
        except Exception as e:
            logger.error(f"Error clearing context: {str(e)}")
            # Don't raise here - clearing context is best effort
