from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Murf API Key
MURF_API_KEY = os.getenv("MURF_API_KEY")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/tts")
async def tts(text: str = Form(...), voiceId: str = Form("en-US-natalie")):
    # Check if API key is set
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    # Correct Murf API endpoint
    url = "https://api.murf.ai/v1/speech/generate"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY
    }

    # Use the voiceId provided by the frontend
    payload = {
        "text": text,
        "voiceId": voiceId,
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "STEREO"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            audio_url = response_data.get("audioFile") or response_data.get("audio_url")
            
            if audio_url:
                return JSONResponse(content={"audio_url": audio_url})
            else:
                return JSONResponse(status_code=500, content={
                    "error": "No audio URL in the API response.", 
                    "response": response_data
                })
        else:
            return JSONResponse(status_code=response.status_code, content={
                "error": "TTS generation failed.", 
                "details": response.text
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "A server error occurred.", "details": str(e)})

@app.get("/voices")
async def get_voices():
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    url = "https://api.murf.ai/v1/speech/voices"
    headers = {
        "Accept": "application/json",
        "api-key": MURF_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            return JSONResponse(status_code=500, content={
                "error": "Failed to fetch voices.", 
                "details": response.text
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "A server error occurred.", "details": str(e)})
