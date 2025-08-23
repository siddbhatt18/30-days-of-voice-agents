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
import time
import threading
import base64

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

# Configure logging - Set to WARNING to reduce clutter
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

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
        print("API keys not configured. Returning fallback audio.")
        return FileResponse(fallback_audio_path, media_type="audio/mpeg", headers={"X-Error": "true"})

    try:
        # Step 1: Transcribe audio to text
        user_query_text = stt.transcribe_audio(audio_file)
        print(f"User: {user_query_text}")

        # Step 2: Retrieve history and get a response from the LLM
        session_history = chat_histories.get(session_id, [])
        llm_response_text, updated_history = llm.get_llm_response(user_query_text, session_history)
        print(f"Assistant: {llm_response_text}")

        # Step 3: Update the chat history
        chat_histories[session_id] = updated_history

        # Step 4: Convert the LLM's text response to speech
        audio_url = tts.convert_text_to_speech(llm_response_text)

        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            raise Exception("TTS service did not return an audio file.")

    except Exception as e:
        print(f"Error in session {session_id}: {e}")
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


async def stream_llm_and_tts(final_text: str, websocket: WebSocket):
    """
    After an end_of_turn transcript, stream Gemini text chunks to the client,
    and for each chunk stream Murf audio (base64) to the client as well.
    """
    full_reply = []

    async for chunk_text in llm.stream_llm_response(final_text):
        if not chunk_text:
            continue

        # 1) stream LLM text chunk to client
        await websocket.send_json({"type": "llm", "text": chunk_text})
        full_reply.append(chunk_text)

        # 2) TTS for the chunk with Murf, send base64 audio
        try:
            audio_bytes = tts.speak(chunk_text)
            if audio_bytes:
                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                await websocket.send_json({"type": "audio", "b64": audio_b64})
        except Exception as tts_err:
            await websocket.send_json({
                "type": "error",
                "message": f"Murf TTS error on chunk: {tts_err}"
            })

    print("\n✅ Full Gemini response:", "".join(full_reply))


@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🎤 Client connected")

    file_path = UPLOADS_DIR / "recorded_audio.webm"
    if file_path.exists():
        file_path.unlink()

    loop = asyncio.get_event_loop()

    async def on_final_async(text: str):
        await websocket.send_json({"type": "final", "text": text})
        await stream_llm_and_tts(text, websocket)

    def on_final(text: str):
        asyncio.run_coroutine_threadsafe(on_final_async(text), loop)

    transcriber = stt.AssemblyAIStreamingTranscriber(
        sample_rate=16000,
        on_final_callback=on_final,
    )

    try:
        with open(file_path, "ab") as f:
            while True:
                data = await websocket.receive_bytes()
                f.write(data)
                transcriber.stream_audio(data)

    except Exception as e:
        print(f"⚠️ WebSocket connection closed: {e}")
        try:
            await websocket.send_json({"type": "info", "message": "WebSocket closed"})
        except Exception:
            pass

    finally:
        transcriber.close()
        print(f"✅ Audio saved at {file_path}")


if __name__ == "__main__":
    import uvicorn
    print("Starting AI Voice Agent Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
