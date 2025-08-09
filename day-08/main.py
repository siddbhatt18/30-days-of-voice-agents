# main.py

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import assemblyai as aai
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Mount static for CSS/JS and templates for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load API Keys from environment variables
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Configure APIs ---

# Configure AssemblyAI
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
else:
    print("Warning: ASSEMBLYAI_API_KEY not found in .env file.")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in .env file.")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/llm/query")
async def llm_query(text: str = Form(...)):
    """
    Receives a text query and returns a response from the Gemini LLM.
    """
    if not GEMINI_API_KEY:
        return JSONResponse(status_code=500, content={"error": "Gemini API key not configured."})

    try:
        # Initialize the Gemini model with the corrected name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(text)

        # Return the generated text
        return JSONResponse(content={"response": response.text})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred with the Gemini API: {str(e)}"})


@app.post("/tts")
async def tts(text: str = Form(...), voiceId: str = Form("en-US-natalie")):
    """
    Generates speech from text using the Murf AI API.
    """
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {"text": text, "voiceId": voiceId, "format": "MP3", "sampleRate": 24000}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        audio_url = response_data.get("audioFile")
        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            return JSONResponse(status_code=500, content={"error": "No audio URL in the API response.", "response": response_data})
    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"error": f"TTS generation failed: {e}"})


@app.get("/voices")
async def get_voices():
    """
    Fetches the list of available voices from the Murf AI API.
    """
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})
    url = "https://api.murf.ai/v1/speech/voices"
    headers = {"Accept": "application/json", "api-key": MURF_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return JSONResponse(content=response.json())
    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to fetch voices: {e}"})


@app.post("/tts/echo")
async def tts_echo(audio_file: UploadFile = File(...)):
    """
    Transcribes audio, then generates speech from the transcription.
    """
    if not ASSEMBLYAI_API_KEY or not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key(s) not configured."})

    try:
        # Step 1: Transcribe with AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription failed: {transcript.error}"})

        transcribed_text = transcript.text
        if not transcribed_text:
            return JSONResponse(status_code=400, content={"error": "No speech detected in the audio."})

        # Step 2: Generate speech with Murf AI
        murf_voice_id = "en-US-natalie" 
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {"text": transcribed_text, "voiceId": murf_voice_id, "format": "MP3"}
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        audio_url = response_data.get("audioFile")

        if audio_url:
            return JSONResponse(content={"audio_url": audio_url, "text": transcribed_text})
        else:
            return JSONResponse(status_code=500, content={"error": "Murf API did not return an audio file.", "details": response_data})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})
