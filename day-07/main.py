# main.py

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import assemblyai as aai

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Mount static for CSS/JS and templates for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load API Keys from environment variables
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Configure AssemblyAI
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
else:
    print("Warning: ASSEMBLYAI_API_KEY not found in .env file.")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# This endpoint is no longer used by the echo bot but is kept for reference
@app.post("/tts")
async def tts(text: str = Form(...), voiceId: str = Form("en-US-natalie")):
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {"text": text, "voiceId": voiceId, "format": "MP3", "sampleRate": 24000}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        response_data = response.json()
        audio_url = response_data.get("audioFile")
        if audio_url:
            return JSONResponse(content={"audio_url": audio_url})
        else:
            return JSONResponse(status_code=500, content={"error": "No audio URL in the API response.", "response": response_data})
    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"error": f"TTS generation failed: {e}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "A server error occurred.", "details": str(e)})


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
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "A server error occurred.", "details": str(e)})


# --- DAY 07 MODIFICATION: New Echo Endpoint ---
@app.post("/tts/echo")
async def tts_echo(audio_file: UploadFile = File(...)):
    if not ASSEMBLYAI_API_KEY or not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key(s) not configured."})

    try:
        # Step 1: Transcribe the audio using AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file.file)

        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription failed: {transcript.error}"})

        transcribed_text = transcript.text
        if not transcribed_text:
            return JSONResponse(status_code=400, content={"error": "No speech detected in the audio."})

        # Step 2: Send the transcription to Murf AI to generate speech
        # For simplicity, we'll use a fixed voice. You can make this a parameter if you want.
        murf_voice_id = "en-US-natalie" 
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {"Content-Type": "application/json", "api-key": MURF_API_KEY}
        payload = {"text": transcribed_text, "voiceId": murf_voice_id, "format": "MP3"}
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes

        response_data = response.json()
        audio_url = response_data.get("audioFile")

        if audio_url:
            # Step 3: Return the URL of the generated audio
            return JSONResponse(content={"audio_url": audio_url, "text": transcribed_text})
        else:
            return JSONResponse(status_code=500, content={"error": "Murf API did not return an audio file.", "details": response_data})

    except requests.exceptions.RequestException as e:
        # This will catch HTTP errors from the Murf API call
        return JSONResponse(status_code=500, content={"error": f"Failed to generate echo speech: {e}"})
    except Exception as e:
        # This will catch other errors, including from AssemblyAI or file handling
        return JSONResponse(status_code=500, content={"error": f"An unexpected error occurred: {str(e)}"})
