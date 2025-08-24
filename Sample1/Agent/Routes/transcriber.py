import time
import google.generativeai as genai
import asyncio
import assemblyai as aai
from Services.Badmosh import MurfStreamer

from assemblyai.streaming.v3 import (
    StreamingClient, StreamingClientOptions,
    StreamingParameters, StreamingSessionParameters,
    StreamingEvents, BeginEvent, TurnEvent,
    TerminationEvent, StreamingError
)
from fastapi import WebSocket


 
aai.settings.api_key = ""
genai.configure(api_key="")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


class AssemblyAIStreamingTranscriber:
    def __init__(self, websocket: WebSocket, loop, sample_rate=16000):
        self.murf = MurfStreamer()
        self.websocket = websocket
        self.loop = loop

        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=aai.settings.api_key,
                api_host="streaming.assemblyai.com"
            )
        )

        self.client.on(StreamingEvents.Begin, self.on_begin)
        self.client.on(StreamingEvents.Turn, self.on_turn)
        self.client.on(StreamingEvents.Termination, self.on_termination)
        self.client.on(StreamingEvents.Error, self.on_error)

    
        self.client.connect(
            StreamingParameters(sample_rate=sample_rate, format_turns=True)
        )

    def on_begin(self, client, event: BeginEvent):
        print(f"🎤 Session started: {event.id}")

    def on_turn(self, client, event: TurnEvent):
        """
        Fire Gemini/Murf ONLY when the turn is formatted (clean sentence),
        and it's the end of user turn.
        """
        print(
            f"{event.transcript} (end_of_turn={event.end_of_turn}, formatted={event.turn_is_formatted})")

        if not event.end_of_turn:
            return

        # If this end-of-turn isn't formatted, request formatting and wait
        if not event.turn_is_formatted:
            client.set_params(StreamingSessionParameters(format_turns=True))
            return

        # Now we have a formatted sentence ayyoooo send to UI and trigger AI response + TTS
        text = (event.transcript or "").strip()
        if not text:
            return

        try:
            asyncio.run_coroutine_threadsafe(
                self.websocket.send_json({"type": "transcript", "text": text}),
                self.loop
            )
            # Start streaming AI response
            self.start_ai_response(text)
        except Exception as e:
            print("⚠️ Failed in on_turn:", e)

    def start_ai_response(self, user_text: str):
        """
        Stream Gemini response and batch it into phrases for Murf.
        This avoids sending single tokens/half-words and ensures Murf emits audio continuously.
        """
        try:
            response = gemini_model.generate_content(
                user_text,
                stream=True
            )

            # Batching controls
            buf = []
            last_flush = time.time()
            FLUSH_MS = 0.25  # ~250ms
            MIN_CHARS = 60   
            SENTENCE_END = ('.', '!', '?', '\n')

            def _flush(final=False):
                nonlocal buf, last_flush
                if not buf:
                    return
                chunk_text = "".join(buf).strip()
                buf.clear()
                last_flush = time.time()
 
             
                asyncio.run_coroutine_threadsafe(
                    self.websocket.send_json(
                        {"type": "ai_response", "text": chunk_text}),
                    self.loop
                )

               
                asyncio.run_coroutine_threadsafe(
                    self.murf.stream_tts(chunk_text, self.websocket),
                    self.loop
                ) if not final else asyncio.run_coroutine_threadsafe(
                    self.murf.stream_tts(chunk_text, self.websocket),
                    self.loop
                )

            for chunk in response:
                if not getattr(chunk, "text", None):
                    continue

                buf.append(chunk.text)

          
                now = time.time()
                text_so_far = "".join(buf)

                should_flush = (
                    len(text_so_far) >= MIN_CHARS or
                    any(text_so_far.rstrip().endswith(p) for p in SENTENCE_END) or
                    (now - last_flush) >= FLUSH_MS
                )

         
                if should_flush and (text_so_far.endswith((" ",) + SENTENCE_END)):
                    _flush(final=False)

         
            if buf:
                _flush(final=True)

        except Exception as e:
            print("⚠️ Gemini streaming error:", e)

    def on_termination(self, client, event: TerminationEvent):
        print(f"🛑 Session terminated after {event.audio_duration_seconds} s")

    def on_error(self, client, error: StreamingError):
        print("❌ Error:", error)

    def stream_audio(self, audio_chunk: bytes):
        self.client.stream(audio_chunk)

    def close(self):
        self.client.disconnect(terminate=True)
