# main.py
from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import asyncio
import base64

# Import services and config
import config
from services import stt, llm, tts

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


async def llm_tts_pipeline(text: str, websocket: WebSocket):
    """
    Manages the concurrent processing of LLM text generation and TTS audio synthesis.
    """
    tts_queue = asyncio.Queue()

    # Task to stream LLM text and push it to the TTS queue
    async def llm_worker():
        try:
            async for chunk in llm.stream_llm_response(text):
                if chunk:
                    await websocket.send_json({"type": "llm", "text": chunk})
                    await tts_queue.put(chunk)
        finally:
            await tts_queue.put(None)  # Signal that LLM is done

    # Task to get text from queue and synthesize audio
    async def tts_worker():
        while True:
            chunk = await tts_queue.get()
            if chunk is None:
                break
            try:
                audio_bytes = tts.speak(chunk)
                if audio_bytes:
                    b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                    await websocket.send_json({"type": "audio", "b64": b64_audio})
            except Exception as e:
                logging.error(f"TTS Error: {e}")
            finally:
                tts_queue.task_done()

    # Start and manage tasks
    await asyncio.gather(
        asyncio.create_task(llm_worker()),
        asyncio.create_task(tts_worker())
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connection for real-time transcription and voice response."""
    await websocket.accept()
    logging.info("WebSocket client connected.")

    # Get the current asyncio event loop
    loop = asyncio.get_event_loop()

    # Callback function for when final transcription is received
    def on_final_transcript(text: str):
        logging.info(f"Final transcript received: {text}")
        # Use run_coroutine_threadsafe to schedule the coroutine from the callback thread
        asyncio.run_coroutine_threadsafe(
            llm_tts_pipeline(text, websocket), loop
        )

    # Initialize the streaming transcriber
    transcriber = stt.AssemblyAIStreamingTranscriber(on_final_callback=on_final_transcript)

    try:
        while True:
            # Receive audio data from the client
            data = await websocket.receive_bytes()
            transcriber.stream_audio(data)
    except Exception as e:
        logging.info(f"WebSocket connection closed: {e}")
    finally:
        transcriber.close()
        logging.info("Transcription resources released.")
