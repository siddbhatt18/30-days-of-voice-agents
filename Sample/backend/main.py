import os
import asyncio
import base64
from fastapi import FastAPI, WebSocket

from utils.logging import setup_logger
from Routes.transcriber import AssemblyAIStreamingTranscriber
from Services.Gemini_service import stream_llm_response
from Services.Tts_service import speak  # uses Murf SDK wrapper

setup_logger()

app = FastAPI()

OUTPUT_DIR = os.path.join("Agent", "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def stream_llm_and_tts(final_text: str, websocket: WebSocket):
    """
    After an end_of_turn transcript, stream Gemini text chunks to the client,
    and for each chunk stream Murf audio (base64) to the client as well.
    """
    full_reply = []

    async for chunk_text in stream_llm_response(final_text):
        if not chunk_text:
            continue

        # 1) stream LLM text chunk to client
        await websocket.send_json({"type": "llm", "text": chunk_text})
        full_reply.append(chunk_text)

        # 2) TTS for the chunk with Murf, send base64 audio
        try:
            audio_bytes = speak(chunk_text)
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

    file_path = os.path.join(OUTPUT_DIR, "recorded_audio.webm")
    if os.path.exists(file_path):
        os.remove(file_path)

    loop = asyncio.get_event_loop()

    async def on_final_async(text: str):
        await websocket.send_json({"type": "final", "text": text})
        await stream_llm_and_tts(text, websocket)

    def on_final(text: str):
        asyncio.run_coroutine_threadsafe(on_final_async(text), loop)

    transcriber = AssemblyAIStreamingTranscriber(
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
