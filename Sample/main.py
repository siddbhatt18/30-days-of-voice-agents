from fastapi import FastAPI, Request, UploadFile, File, Path, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import os
import uuid
import uvicorn
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

from models.schemas import (
    VoiceChatResponse, 
    ChatHistoryResponse, 
    BackendStatusResponse,
    APIKeyConfig,
    ErrorType
)
from services.stt_service import STTService
from services.llm_service import LLMService
from services.tts_service import TTSService
from services.database_service import DatabaseService
from services.assemblyai_streaming_service import AssemblyAIStreamingService
from services.murf_websocket_service import MurfWebSocketService
from utils.logging_config import setup_logging, get_logger
from utils.constants import get_fallback_message

# Load environment variables
load_dotenv()
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="30 Days of Voice Agents - FastAPI",
    description="A modern conversational AI voice agent with FastAPI backend",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
stt_service: STTService = None
llm_service: LLMService = None
tts_service: TTSService = None
database_service: DatabaseService = None
assemblyai_streaming_service: AssemblyAIStreamingService = None
murf_websocket_service: MurfWebSocketService = None


def initialize_services() -> APIKeyConfig:
    """Initialize all services with API keys"""
    config = APIKeyConfig(
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        assemblyai_api_key=os.getenv("ASSEMBLYAI_API_KEY"),
        murf_api_key=os.getenv("MURF_API_KEY"),
        murf_voice_id=os.getenv("MURF_VOICE_ID", "en-IN-aarav"),
        mongodb_url=os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    )
    
    global stt_service, llm_service, tts_service, database_service, assemblyai_streaming_service, murf_websocket_service
    if config.are_keys_valid:
        stt_service = STTService(config.assemblyai_api_key)
        llm_service = LLMService(config.gemini_api_key)
        tts_service = TTSService(config.murf_api_key, config.murf_voice_id)
        assemblyai_streaming_service = AssemblyAIStreamingService(config.assemblyai_api_key)
        murf_websocket_service = MurfWebSocketService(config.murf_api_key, config.murf_voice_id)
        logger.info("✅ All AI services initialized successfully")
    else:
        missing_keys = config.validate_keys()
        logger.error(f"❌ Missing API keys: {missing_keys}")
    database_service = DatabaseService(config.mongodb_url)
    
    return config


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Voice Agent application...")
    
    config = initialize_services()
    if database_service:
        await database_service.connect()
    
    logger.info("✅ Application startup completed")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 Shutting down Voice Agent application...")
    
    if database_service:
        await database_service.close()
    
    logger.info("✅ Application shutdown completed")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main application page"""
    session_id = request.query_params.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    
    logger.info(f"Serving home page for session: {session_id}")
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "session_id": session_id
    })


@app.get("/api/backend", response_model=BackendStatusResponse)
async def get_backend_status():
    """Get backend status"""
    try:
        return BackendStatusResponse(
            status="healthy",
            services={
                "stt": stt_service is not None,
                "llm": llm_service is not None,
                "tts": tts_service is not None,
                "database": database_service is not None,
                "assemblyai_streaming": assemblyai_streaming_service is not None,
                "murf_websocket": murf_websocket_service is not None
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting backend status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/agent/chat/{session_id}/history", response_model=ChatHistoryResponse)
async def get_chat_history_endpoint(session_id: str = Path(..., description="Session ID")):
    """Get chat history for a session"""
    try:
        chat_history = await database_service.get_chat_history(session_id)
        return ChatHistoryResponse(
            success=True,
            session_id=session_id,
            messages=chat_history,
            message_count=len(chat_history)
        )
    except Exception as e:
        logger.error(f"Error getting chat history for session {session_id}: {str(e)}")
        return ChatHistoryResponse(
            success=False,
            session_id=session_id,
            messages=[],
            message_count=0
        )


@app.post("/agent/chat/{session_id}", response_model=VoiceChatResponse)
async def chat_with_agent(
    session_id: str = Path(..., description="Session ID"),
    audio: UploadFile = File(..., description="Audio file for voice input")
):
    """Chat with the voice agent using audio input"""
    transcribed_text = ""
    response_text = ""
    audio_url = None
    
    try:
        # Get services status for better error handling
        config = initialize_services()
        
        if not config.are_keys_valid:
            missing_keys = config.validate_keys()
            logger.error(f"Missing API keys for session {session_id}: {missing_keys}")
            if tts_service:
                fallback_audio = await tts_service.generate_fallback_audio(
                    get_fallback_message(ErrorType.API_KEYS_MISSING)
                )
            return VoiceChatResponse(
                success=False,
                message=get_fallback_message(ErrorType.API_KEYS_MISSING),
                transcription="",
                llm_response=get_fallback_message(ErrorType.API_KEYS_MISSING),
                audio_url=fallback_audio,
                session_id=session_id,
                error_type=ErrorType.API_KEYS_MISSING
            )
        
        # Save uploaded audio file temporarily
        audio_content = await audio.read()
        temp_audio_path = f"temp_audio_{session_id}_{uuid.uuid4().hex}.wav"
        
        try:
            with open(temp_audio_path, "wb") as temp_file:
                temp_file.write(audio_content)
        except Exception as e:
            logger.error(f"Error saving temp audio for session {session_id}: {str(e)}")
            fallback_audio = None
            if tts_service:
                fallback_audio = await tts_service.generate_fallback_audio(
                    get_fallback_message(ErrorType.FILE_ERROR)
                )
            return VoiceChatResponse(
                success=False,
                message=get_fallback_message(ErrorType.FILE_ERROR),
                transcription="",
                llm_response=get_fallback_message(ErrorType.FILE_ERROR),
                audio_url=fallback_audio,
                session_id=session_id,
                error_type=ErrorType.FILE_ERROR
            )
        
        # Transcribe audio to text
        try:
            transcribed_text = await stt_service.transcribe_audio(temp_audio_path)
            logger.info(f"Transcription successful for session {session_id}: {transcribed_text[:100]}")
        except Exception as e:
            logger.error(f"STT error for session {session_id}: {str(e)}")
            if tts_service:
                fallback_audio = await tts_service.generate_fallback_audio(
                    get_fallback_message(ErrorType.STT_ERROR)
                )
            return VoiceChatResponse(
                success=False,
                message=get_fallback_message(ErrorType.STT_ERROR),
                transcription="",
                llm_response=get_fallback_message(ErrorType.STT_ERROR),
                audio_url=fallback_audio,
                session_id=session_id,
                error_type=ErrorType.STT_ERROR
            )
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_audio_path}: {str(e)}")
        
        # Generate LLM response
        try:
            chat_history = await database_service.get_chat_history(session_id)
            await database_service.add_message_to_history(session_id, "user", transcribed_text)
            response_text = await llm_service.generate_response(transcribed_text, chat_history)
            await database_service.add_message_to_history(session_id, "assistant", response_text)
            logger.info(f"LLM response generated for session {session_id}: {response_text[:100]}")
        except Exception as e:
            logger.error(f"LLM error for session {session_id}: {str(e)}")
            response_text = get_fallback_message(ErrorType.LLM_ERROR)
        
        # Generate TTS audio
        try:
            audio_url = await tts_service.generate_audio(response_text, session_id)
            logger.info(f"TTS audio generated for session {session_id}: {audio_url}")
        except Exception as e:
            logger.error(f"TTS error for session {session_id}: {str(e)}")
            fallback_audio = await tts_service.generate_fallback_audio(
                get_fallback_message(ErrorType.TTS_ERROR)
            )
            return VoiceChatResponse(
                success=False,
                message=get_fallback_message(ErrorType.TTS_ERROR),
                transcription=transcribed_text,
                llm_response=response_text,
                audio_url=fallback_audio,
                error_type=ErrorType.TTS_ERROR
            )
        logger.info(f"Voice chat completed successfully for session: {session_id}")
        return VoiceChatResponse(
            success=True,
            message="Voice chat processed successfully",
            transcription=transcribed_text,
            llm_response=response_text,
            audio_url=audio_url,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in chat_with_agent: {str(e)}")
        fallback_audio = None
        if tts_service:
            fallback_audio = await tts_service.generate_fallback_audio(
                get_fallback_message(ErrorType.GENERAL_ERROR)
            )
        
        return VoiceChatResponse(
            success=False,
            message=get_fallback_message(ErrorType.GENERAL_ERROR),
            transcription=transcribed_text,
            llm_response=get_fallback_message(ErrorType.GENERAL_ERROR),
            audio_url=fallback_audio,
            error_type=ErrorType.GENERAL_ERROR
        )
        

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    def is_connected(self, websocket: WebSocket) -> bool:
        """Check if a WebSocket is still in active connections"""
        return websocket in self.active_connections

    async def send_personal_message(self, message: str, websocket: WebSocket):
        if self.is_connected(websocket):
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error sending personal message: {e}")
                self.disconnect(websocket)
        else:
            logger.debug("Attempted to send message to disconnected WebSocket")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                self.disconnect(connection)


manager = ConnectionManager()

# Global locks to prevent concurrent LLM streaming for the same session
session_locks = {}

# Global function to handle LLM streaming (moved outside WebSocket handler to prevent duplicates)
async def handle_llm_streaming(user_message: str, session_id: str, websocket: WebSocket):
    """Handle LLM streaming response and send to Murf WebSocket for TTS"""
    
    # Prevent concurrent streaming for the same session
    if session_id not in session_locks:
        session_locks[session_id] = asyncio.Lock()
    
    async with session_locks[session_id]:
        print(f"🔒 Acquired session lock for: {session_id}")
        
        # Initialize variables at function scope to avoid UnboundLocalError
        accumulated_response = ""
        audio_chunk_count = 0
        total_audio_size = 0
        
        print(f"🤖 Starting LLM streaming for: {user_message}")
        
        try:
            # Get chat history
            try:
                chat_history = await database_service.get_chat_history(session_id)
                await database_service.add_message_to_history(session_id, "user", user_message)
            except Exception as e:
                logger.error(f"Chat history error: {str(e)}")
                chat_history = []
            
            # Send LLM streaming start notification
            start_message = {
                "type": "llm_streaming_start",
                "message": "LLM is generating response...",
                "user_message": user_message,
                "timestamp": datetime.now().isoformat()
            }
            await manager.send_personal_message(json.dumps(start_message), websocket)
            
            # Connect to Murf WebSocket
            try:
                await murf_websocket_service.connect()
                logger.info("Connected to Murf WebSocket for streaming TTS")
                
                # Create async generator for LLM streaming
                async def llm_text_stream():
                    nonlocal accumulated_response
                    async for chunk in llm_service.generate_streaming_response(user_message, chat_history):
                        if chunk:
                            accumulated_response += chunk
                            print(f"🤖 LLM chunk: {chunk}", end="", flush=True)
                            
                            # Send chunk to client
                            chunk_message = {
                                "type": "llm_streaming_chunk",
                                "chunk": chunk,
                                "accumulated_length": len(accumulated_response),
                                "timestamp": datetime.now().isoformat()
                            }
                            await manager.send_personal_message(json.dumps(chunk_message), websocket)
                            
                            yield chunk
                
                # Send LLM stream to Murf and receive base64 audio
                tts_start_message = {
                    "type": "tts_streaming_start", 
                    "message": "Starting TTS streaming with Murf WebSocket...",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(json.dumps(tts_start_message), websocket)
                
                # Stream LLM text to Murf and get base64 audio back
                async for audio_response in murf_websocket_service.stream_text_to_audio(llm_text_stream()):
                    if audio_response["type"] == "audio_chunk":
                        audio_chunk_count += 1
                        total_audio_size += audio_response["chunk_size"]
                        
                        # Send audio data to client
                        audio_message = {
                            "type": "tts_audio_chunk",
                            "audio_base64": audio_response["audio_base64"],
                            "chunk_number": audio_response["chunk_number"],
                            "chunk_size": audio_response["chunk_size"],
                            "total_size": audio_response["total_size"],
                            "is_final": audio_response["is_final"],
                            "timestamp": audio_response["timestamp"]
                        }
                        await manager.send_personal_message(json.dumps(audio_message), websocket)
                        
                        # Check if this is the final chunk
                        if audio_response["is_final"]:
                            print(f"\n🎵 TTS streaming completed. Total audio chunks: {audio_chunk_count}")
                            break
                    
                    elif audio_response["type"] == "status":
                        # Send status updates to client
                        status_message = {
                            "type": "tts_status",
                            "data": audio_response["data"],
                            "timestamp": audio_response["timestamp"]
                        }
                        await manager.send_personal_message(json.dumps(status_message), websocket)
                
            except Exception as e:
                logger.error(f"Error with Murf WebSocket streaming: {str(e)}")
                error_message = {
                    "type": "tts_streaming_error",
                    "message": f"Error with Murf WebSocket: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.send_personal_message(json.dumps(error_message), websocket)
            
            finally:
                # Disconnect from Murf WebSocket
                try:
                    await murf_websocket_service.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting from Murf WebSocket: {str(e)}")
            
            print()
            print(f"🤖 LLM streaming completed. Total response: {len(accumulated_response)} characters")
            
            # Save to chat history
            try:
                await database_service.add_message_to_history(session_id, "assistant", accumulated_response)
            except Exception as e:
                logger.error(f"Failed to save assistant response to history: {str(e)}")
            
            # Send completion notification
            complete_message = {
                "type": "llm_streaming_complete",
                "message": "LLM response and TTS streaming completed",
                "complete_response": accumulated_response,
                "total_length": len(accumulated_response),
                "audio_chunks_received": audio_chunk_count,
                "total_audio_size": total_audio_size,
                "timestamp": datetime.now().isoformat()
            }
            await manager.send_personal_message(json.dumps(complete_message), websocket)
            
        except Exception as e:
            logger.error(f"Error in LLM streaming: {str(e)}")
            error_message = {
                "type": "llm_streaming_error",
                "message": f"Error generating LLM response: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            await manager.send_personal_message(json.dumps(error_message), websocket)
        
        finally:
            print(f"🔓 Released session lock for: {session_id}")


@app.websocket("/ws/audio-stream")
async def audio_stream_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    session_id = str(uuid.uuid4())
    audio_filename = f"streamed_audio_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    audio_filepath = os.path.join("streamed_audio", audio_filename)
    os.makedirs("streamed_audio", exist_ok=True)
    is_websocket_active = True
    last_processed_transcript = ""  # Track last processed transcript to prevent duplicates
    last_processing_time = 0  # Track when we last processed a transcript
    
    async def transcription_callback(transcript_data):
        nonlocal last_processed_transcript, last_processing_time
        try:
            if is_websocket_active and manager.is_connected(websocket):
                await manager.send_personal_message(json.dumps(transcript_data), websocket)
                # Only show final transcriptions and trigger LLM streaming
                if transcript_data.get("type") == "final_transcript":
                    final_text = transcript_data.get('text', '').strip()
                    print(f"📝 Final transcript: {final_text}")
                    
                    # Normalize text for comparison (remove punctuation, convert to lowercase)
                    normalized_current = final_text.lower().strip('.,!?;: ')
                    normalized_last = last_processed_transcript.lower().strip('.,!?;: ')
                    
                    # Add cooldown period (minimum 2 seconds between processing)
                    current_time = datetime.now().timestamp()
                    time_since_last = current_time - last_processing_time
                    
                    # Prevent duplicate processing of the same or very similar transcript
                    if (final_text and 
                        normalized_current != normalized_last and 
                        len(normalized_current) > 0 and 
                        time_since_last >= 2.0 and  # 2 second cooldown
                        llm_service):
                        
                        last_processed_transcript = final_text
                        last_processing_time = current_time
                        print(f"🔄 Processing new transcript: {final_text}")
                        await handle_llm_streaming(final_text, session_id, websocket)
                    elif normalized_current == normalized_last:
                        print(f"⚠️ Skipping duplicate/similar transcript: {final_text} (already processed: {last_processed_transcript})")
                    elif time_since_last < 2.0:
                        print(f"⚠️ Skipping transcript due to cooldown: {final_text} (last processed {time_since_last:.1f}s ago)")
                    elif len(normalized_current) == 0:
                        print(f"⚠️ Skipping empty transcript: '{final_text}'")
                        
            else:
                logger.debug("Skipping transcription callback - WebSocket no longer active")
        except Exception as e:
            logger.error(f"Error sending transcription: {e}")

    try:
        if assemblyai_streaming_service:
            assemblyai_streaming_service.set_transcription_callback(transcription_callback)
            async def safe_websocket_callback(msg):
                if is_websocket_active and manager.is_connected(websocket):
                    return await manager.send_personal_message(json.dumps(msg), websocket)
                return None
            
            await assemblyai_streaming_service.start_streaming_transcription(
                websocket_callback=safe_websocket_callback
            )
        
        welcome_message = {
            "type": "audio_stream_ready",
            "message": "Audio streaming endpoint ready with AssemblyAI transcription. Send binary audio data.",
            "session_id": session_id,
            "audio_filename": audio_filename,
            "transcription_enabled": assemblyai_streaming_service is not None,
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_personal_message(json.dumps(welcome_message), websocket)
        logger.info(f"Audio streaming session started: {session_id}")
        
        with open(audio_filepath, "wb") as audio_file:
            chunk_count = 0
            total_bytes = 0
            
            while True:
                try:
                    message = await websocket.receive()
                    
                    if "text" in message:
                        command = message["text"]
                        
                        if command == "start_streaming":
                            response = {
                                "type": "command_response",
                                "message": "Ready to receive audio chunks with real-time transcription",
                                "status": "streaming_ready"
                            }
                            await manager.send_personal_message(json.dumps(response), websocket)
                            
                        elif command == "stop_streaming":
                            response = {
                                "type": "command_response",
                                "message": "Stopping audio stream",
                                "status": "streaming_stopped"
                            }
                            await manager.send_personal_message(json.dumps(response), websocket)
                            
                            if assemblyai_streaming_service:
                                async def safe_stop_callback(msg):
                                    if manager.is_connected(websocket):
                                        return await manager.send_personal_message(json.dumps(msg), websocket)
                                    return None
                            break
                    
                    elif "bytes" in message:
                        audio_chunk = message["bytes"]
                        chunk_count += 1
                        total_bytes += len(audio_chunk)
                        
                        # Write to file
                        audio_file.write(audio_chunk)
                        
                        # Send to AssemblyAI for transcription if available
                        if assemblyai_streaming_service and is_websocket_active:
                            await assemblyai_streaming_service.send_audio_chunk(audio_chunk)
                        
                        # Send chunk confirmation to client
                        if chunk_count % 10 == 0:  # Send every 10th chunk to avoid spam
                            chunk_response = {
                                "type": "audio_chunk_received",
                                "chunk_number": chunk_count,
                                "total_bytes": total_bytes,
                                "timestamp": datetime.now().isoformat()
                            }
                            await manager.send_personal_message(json.dumps(chunk_response), websocket)
                
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"Error processing audio chunk: {e}")
                    break
        
        final_response = {
            "type": "audio_stream_complete",
            "message": f"Audio stream completed. Total chunks: {chunk_count}, Total bytes: {total_bytes}",
            "session_id": session_id,
            "audio_filename": audio_filename,
            "total_chunks": chunk_count,
            "total_bytes": total_bytes,
            "timestamp": datetime.now().isoformat()
        }
        await manager.send_personal_message(json.dumps(final_response), websocket)
        
    except WebSocketDisconnect:
        is_websocket_active = False
        manager.disconnect(websocket)
        logger.info(f"Audio streaming WebSocket disconnected for session: {session_id}")
    except Exception as e:
        is_websocket_active = False
        logger.error(f"Audio streaming WebSocket error: {e}")
        manager.disconnect(websocket)
    finally:
        is_websocket_active = False
        if assemblyai_streaming_service:
            await assemblyai_streaming_service.stop_streaming_transcription()
        logger.info(f"Audio streaming session ended: {session_id}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
