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
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
else:
    print("Warning: ASSEMBLYAI_API_KEY not found in .env file.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in .env file.")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/llm/query")
async def llm_query(audio_file: UploadFile = File(...)):
    if not (GEMINI_API_KEY and ASSEMBLYAI_API_KEY and MURF_API_KEY):
        return JSONResponse(status_code=500, content={"error": "One or more API keys are not configured."})

    try:
        # Step 1: Transcribe audio to text with AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription failed: {transcript.error}"})

        user_query_text = transcript.text
        if not user_query_text:
            return JSONResponse(status_code=400, content={"error": "No speech detected in the audio."})

        # Step 2: Get a response from the Gemini LLM
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(user_query_text)
        llm_response_text = response.text

        # Step 3: Convert the LLM's text response to speech with Murf AI
        murf_voice_id = "en-US-natalie"
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {
            "text": llm_response_text,
            "voiceId": murf_voice_id,
            "format": "MP3",
            "volume": "100%"  # Set volume to maximum
        }

        murf_response = requests.post(url, json=payload, headers=headers)
        murf_response.raise_for_status()
        response_data = murf_response.json()
        audio_url = response_data.get("audioFile")

        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            return JSONResponse(status_code=500, content={"error": "Murf API did not return an audio file."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})


@app.post("/tts")
async def tts(text: str = Form(...), voiceId: str = Form("en-US-natalie")):
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {
        "text": text,
        "voiceId": voiceId,
        "format": "MP3",
        "sampleRate": 24000,
        "volume": "100%"  # Set volume to maximum
    }
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
    if not ASSEMBLYAI_API_KEY or not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key(s) not configured."})
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)
        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription failed: {transcript.error}"})
        transcribed_text = transcript.text
        if not transcribed_text:
            return JSONResponse(status_code=400, content={"error": "No speech detected in the audio."})
        
        murf_voice_id = "en-US-natalie"
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {
            "text": transcribed_text,
            "voiceId": murf_voice_id,
            "format": "MP3",
            "volume": "100%"  # Set volume to maximum
        }
        
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
