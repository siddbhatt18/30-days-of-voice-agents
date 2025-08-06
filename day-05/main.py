from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import shutil

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# --- MODIFICATION 1: Mount both static and uploads directories ---
# Mount static for CSS/JS and templates for HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
# Mount uploads to make uploaded files accessible via a URL
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")


# Ensure the 'uploads' directory exists
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Load Murf API Key from environment variables
MURF_API_KEY = os.getenv("MURF_API_KEY")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# (The /tts and /voices endpoints remain unchanged)
@app.post("/tts")
async def tts(text: str = Form(...), voiceId: str = Form("en-US-natalie")):
    if not MURF_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "api-key": MURF_API_KEY}
    payload = {"text": text, "voiceId": voiceId, "format": "MP3", "sampleRate": 24000}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            audio_url = response_data.get("audioFile")
            if audio_url:
                return JSONResponse(content={"audio_url": audio_url})
            else:
                return JSONResponse(status_code=500, content={"error": "No audio URL in the API response.", "response": response_data})
        else:
            return JSONResponse(status_code=response.status_code, content={"error": "TTS generation failed.", "details": response.text})
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
        if response.status_code == 200:
            return JSONResponse(content=response.json())
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to fetch voices.", "details": response.text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "A server error occurred.", "details": str(e)})


@app.post("/upload-audio")
async def upload_audio(audio_file: UploadFile = File(...)):
    file_path = os.path.join(UPLOADS_DIR, audio_file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        file_size = os.path.getsize(file_path)

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Could not save file: {e}"})
    finally:
        await audio_file.close()

    # --- MODIFICATION 2: Construct a URL and add it to the response ---
    # This URL points to the file now being served from the /uploads directory
    file_url = f"/uploads/{audio_file.filename}"

    return {
        "filename": audio_file.filename,
        "content_type": audio_file.content_type,
        "size": file_size,
        "file_url": file_url, # The new URL for the frontend to use
    }
