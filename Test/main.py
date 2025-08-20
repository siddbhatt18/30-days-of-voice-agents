# main.py
from fastapi import FastAPI, Request, UploadFile, File, Path, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, List, Any, Type
import logging
from pathlib import Path as PathLib
from uuid import uuid4
import json
import asyncio

# Import the config file FIRST to load dotenv and configure APIs
import config
from services import stt, llm, tts
from schemas import TTSRequest

# AssemblyAI streaming imports
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Mount static for CSS/JS and templates for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory store for chat histories.
chat_histories: Dict[str, List[Dict[str, Any]]] = {}

# Base directory and uploads folder
BASE_DIR = PathLib(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@app.get("/")
async def home(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/agent/chat/{session_id}")
async def agent_chat(
    session_id: str = Path(..., description="The unique ID for the chat session."),
    audio_file: UploadFile = File(...)
):
    """
    Handles a turn in the conversation, including history.
    STT -> Add to History -> LLM -> Add to History -> TTS
    """
    fallback_audio_path = "static/fallback.mp3"

    # Check for keys by importing them from the config module
    if not all([config.GEMINI_API_KEY, config.ASSEMBLYAI_API_KEY, config.MURF_API_KEY]):
        logging.warning("One or more API keys are not configured. Returning fallback audio.")
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})

    try:
        # Step 1: Transcribe audio to text
        user_query_text = stt.transcribe_audio(audio_file)
        logging.info(f"User Query (session {session_id}): {user_query_text}")

        # Step 2: Retrieve history and get a response from the LLM
        session_history = chat_histories.get(session_id, [])
        llm_response_text, updated_history = llm.get_llm_response(user_query_text, session_history)
        logging.info(f"LLM Response (session {session_id}): {llm_response_text}")

        # Step 3: Update the chat history
        chat_histories[session_id] = updated_history

        # Step 4: Convert the LLM's text response to speech
        audio_url = tts.convert_text_to_speech(llm_response_text)

        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            raise Exception("TTS service did not return an audio file.")

    except Exception as e:
        logging.error(f"An error occurred in session {session_id}: {e}")
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})


@app.post("/tts")
async def tts_endpoint(request: TTSRequest):
    """Endpoint for the simple Text-to-Speech utility."""
    try:
        audio_url = tts.convert_text_to_speech(request.text, request.voiceId)
        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            return JSONResponse(status_code=500, content={"error": "No audio URL in the API response."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"TTS generation failed: {e}"})


@app.get("/voices")
async def get_voices():
    """Fetches the list of available voices from Murf AI."""
    try:
        voices = tts.get_available_voices()
        return JSONResponse(content={"voices": voices})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to fetch voices: {e}"})


@app.websocket("/ws")
async def websocket_audio_streaming(websocket: WebSocket):
    """Receive PCM audio chunks from client and transcribe in real-time using AssemblyAI with turn detection."""
    await websocket.accept()
    file_id = uuid4().hex
    file_path = UPLOADS_DIR / f"streamed_{file_id}.pcm"

    # Check if AssemblyAI API key is configured
    if not config.ASSEMBLYAI_API_KEY:
        logging.error("ASSEMBLYAI_API_KEY not configured")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": "AssemblyAI API key not configured"
        }))
        await websocket.close(code=1000, reason="AssemblyAI API key not configured")
        return

    # Create a queue for transcription messages
    transcription_queue = asyncio.Queue()

    # Initialize AssemblyAI StreamingClient
    client = StreamingClient(
        StreamingClientOptions(
            api_key=config.ASSEMBLYAI_API_KEY,
            api_host="streaming.assemblyai.com",
        )
    )

    # Define event handlers
    def on_begin(self: Type[StreamingClient], event: BeginEvent):
        logging.info(f"Transcription session started: {event.id}")

    def on_turn(self: Type[StreamingClient], event: TurnEvent):
        transcript_text = event.transcript
        logging.info(f"Real-time transcript: {transcript_text}")
        print(f"TRANSCRIPTION: {transcript_text}")  # Print to console as requested
        
        # Only send transcription to client when turn ends (turn detection)
        if event.end_of_turn:
            logging.info(f"End of turn detected. Final transcript: {transcript_text}")
            print(f"END OF TURN - FINAL TRANSCRIPTION: {transcript_text}")
            
            # Put final transcription in queue for async sending
            try:
                transcription_queue.put_nowait({
                    "type": "transcription",
                    "text": transcript_text,
                    "is_final": True,
                    "end_of_turn": True
                })
                
                # Send explicit end-of-turn notification
                transcription_queue.put_nowait({
                    "type": "turn_end",
                    "message": "User stopped talking"
                })
            except asyncio.QueueFull:
                logging.warning("Transcription queue is full")
        
        # Configure turn formatting if not already done
        if event.end_of_turn and not event.turn_is_formatted:
            params = StreamingParameters(
                sample_rate=16000, 
                format_turns=True,
                enable_extra_session_information=True
            )
            self.set_params(params)

    def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
        logging.info(f"Transcription session terminated: {event.audio_duration_seconds} seconds of audio processed")

    def on_error(self: Type[StreamingClient], error: StreamingError):
        logging.error(f"AssemblyAI streaming error: {error}")
        try:
            transcription_queue.put_nowait({
                "type": "error",
                "message": f"Transcription error: {error}"
            })
        except asyncio.QueueFull:
            logging.warning("Transcription queue is full")

    # Register event handlers
    client.on(StreamingEvents.Begin, on_begin)
    client.on(StreamingEvents.Turn, on_turn)
    client.on(StreamingEvents.Termination, on_terminated)
    client.on(StreamingEvents.Error, on_error)

    # Task to send transcription messages to client
    async def send_transcriptions():
        while True:
            try:
                message = await asyncio.wait_for(transcription_queue.get(), timeout=0.1)
                await websocket.send_text(json.dumps(message))
                transcription_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logging.error(f"Error sending transcription: {e}")
                break

    # Start the transcription sender task
    sender_task = asyncio.create_task(send_transcriptions())

    # Connect to AssemblyAI streaming service
    try:
        client.connect(
            StreamingParameters(
                sample_rate=16000,
                format_turns=True,
                enable_extra_session_information=True,
            )
        )
        
        logging.info("Connected to AssemblyAI streaming service with turn detection enabled")
        await websocket.send_text(json.dumps({
            "type": "status",
            "message": "Connected to transcription service with turn detection"
        }))

        # Save audio to file for debugging (optional)
        with open(file_path, "wb") as f:
            while True:
                message = await websocket.receive()
                
                if "bytes" in message:
                    pcm_data = message["bytes"]
                    logging.debug(f"Received audio chunk of size: {len(pcm_data)} bytes")
                    f.write(pcm_data)  # Save to file for debugging
                    client.stream(pcm_data)  # Send to AssemblyAI for transcription
                    
                elif message.get("text") == "EOF":
                    logging.info("Recording finished. Closing transcription session.")
                    break

    except WebSocketDisconnect:
        logging.info("Client disconnected from WebSocket")
    except Exception as e:
        logging.error(f"WebSocket error: {str(e)}")
    finally:
        # Cancel the sender task
        sender_task.cancel()
        
        # Clean up AssemblyAI connection
        try:
            client.disconnect(terminate=True)
        except Exception as e:
            logging.error(f"Error disconnecting from AssemblyAI: {e}")
        
        # Close WebSocket connection
        try:
            await websocket.close()
        except Exception as e:
            logging.error(f"Error closing WebSocket: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
