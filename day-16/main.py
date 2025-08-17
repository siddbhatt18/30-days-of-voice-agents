# main.py
from fastapi import FastAPI, Request, UploadFile, File, Path, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, List, Any
import logging

# Import the config file FIRST to load dotenv and configure APIs
import config
from services import stt, llm, tts
from schemas import TTSRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Mount static for CSS/JS and templates for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory store for chat histories.
chat_histories: Dict[str, List[Dict[str, Any]]] = {}


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
async def websocket_endpoint(websocket: WebSocket):
    """Establishes a WebSocket connection and saves incoming audio."""
    await websocket.accept()
    try:
        with open("output.webm", "wb") as f:
            while True:
                data = await websocket.receive_bytes()
                f.write(data)
    except WebSocketDisconnect:
        logging.info("WebSocket connection closed")
