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
async def tts(text: str = Form(...)):
    # Check if API key is set
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    # Correct Murf API endpoint
    url = "https://api.murf.ai/v1/speech/generate"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY  # Note: header is 'api-key', not 'apikey'
    }

    # Correct payload format for Murf API
    payload = {
        "text": text,
        "voiceId": "en-US-natalie",  # Use a valid Murf voice ID
        "format": "MP3",  # Specify audio format
        "sampleRate": 24000,  # Sample rate
        "channelType": "STEREO"  # Channel type
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            # The response structure may vary, check for different possible keys
            audio_url = response_data.get("audioFile") or response_data.get("audio_url") or response_data.get("url")
            
            if audio_url:
                return JSONResponse(content={"audio_url": audio_url})
            else:
                return JSONResponse(status_code=500, content={
                    "error": "No audio URL in response", 
                    "response": response_data
                })
        else:
            print(f"TTS Error: {response.status_code} - {response.text}")
            return JSONResponse(status_code=500, content={
                "error": "TTS failed", 
                "details": response.text,
                "status_code": response.status_code
            })
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})

# Optional: Add endpoint to get available voices
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
                "error": "Failed to fetch voices", 
                "details": response.text
            })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Server error", "details": str(e)})
