import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from Routes import agent_chat
from utils.logging import setup_logger
from Routes.transcriber import AssemblyAIStreamingTranscriber

setup_logger()

app = FastAPI()

OUTPUT_DIR = os.path.join("Agent", "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def get_homepage():
    return FileResponse("index.html", media_type="text/html")


@app.get("/style.css")
def get_style():
    return FileResponse("style.css", media_type="text/css")


@app.get("/script.js")
def get_script():
    return FileResponse("script.js", media_type="application/javascript")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🎤 Client connected")

    loop = asyncio.get_running_loop()
    transcriber = AssemblyAIStreamingTranscriber(
        websocket, loop, sample_rate=16000)

    try:
        while True:
            data = await websocket.receive_bytes()
            transcriber.stream_audio(data)

    except Exception as e:
        print(f"⚠️ WebSocket connection closed: {e}")

    finally:
        transcriber.close()


# Include API routes
app.include_router(agent_chat.router)
