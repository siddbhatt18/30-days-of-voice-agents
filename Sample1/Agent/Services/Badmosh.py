import asyncio
import websockets
import json
import os

MURF_API_KEY = os.getenv(
    "MURF_API_KEY") or "apna key dalo yaar"
MURF_WS_URL = "wss://api.murf.ai/v1/speech/stream-input"


class MurfStreamer:
    def __init__(self, voice_id="en-US-ken", context_id="static-context-123"):
        self.voice_id = voice_id
        self.context_id = context_id
        self.ws = None

    async def connect(self):
        if not self.ws:
            print("🔌 Connecting to Murf WebSocket...")
            self.ws = await websockets.connect(
                f"{MURF_WS_URL}?api-key={MURF_API_KEY}&sample_rate=44100&channel_type=MONO&format=WAV&context_id={self.context_id}"
            )
            voice_config_msg = {
                "voice_config": {
                    "voiceId": self.voice_id,
                    "rate": 0,
                    "pitch": 0,
                    "variation": 1,
                    "style": "Conversational",
                }
            }
            await self.ws.send(json.dumps(voice_config_msg))
            print("✅ Voice config sent to Murf")

    async def stream_tts(self, text: str, websocket: websockets, final=False):
        await self.connect()

        # send text chunk
        text_msg = {
            "text": text,
            "end": final   
        }
        await self.ws.send(json.dumps(text_msg))
        print(
            f"📨 Sent text to Murf: {text[:50]}{'...' if len(text) > 50 else ''}")

        while True:
            response = await self.ws.recv()
            data = json.loads(response)

            if "audio" in data:
                print(f"🎶 Received audio chunk (len={len(data['audio'])})")
                await websocket.send_json({
                    "type": "audio_chunk",
                    "audio": data["audio"]
                })

            if data.get("final"):
                print("🏁 Murf marked response as final")
                break
