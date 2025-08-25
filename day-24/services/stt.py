# services/stt.py
import assemblyai as aai
from fastapi import UploadFile
import os
from dotenv import load_dotenv
from assemblyai.streaming.v3 import (
    StreamingClient,
    StreamingClientOptions,
    StreamingParameters,
    StreamingSessionParameters,
    StreamingEvents,
    BeginEvent,
    TurnEvent,
    TerminationEvent,
    StreamingError,
)

load_dotenv()

# expects ASSEMBLYAI_API_KEY in env
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY") or ""


def _on_begin(client: StreamingClient, event: BeginEvent):
    print(f"AAI session started: {event.id}")


def _on_termination(client: StreamingClient, event: TerminationEvent):
    print(f"AAI session terminated after {event.audio_duration_seconds} s")


def _on_error(client: StreamingClient, error: StreamingError):
    print("AAI error:", error)


class AssemblyAIStreamingTranscriber:
    """
    Wrapper around AAI StreamingClient that exposes:
      - on_partial_callback(text) for interim results
      - on_final_callback(text)   when end_of_turn=True
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        on_partial_callback=None,
        on_final_callback=None,
    ):
        self.on_partial_callback = on_partial_callback
        self.on_final_callback = on_final_callback

        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=aai.settings.api_key,
                api_host="streaming.assemblyai.com",
            )
        )

        # register events
        self.client.on(StreamingEvents.Begin, _on_begin)
        self.client.on(StreamingEvents.Error, _on_error)
        self.client.on(StreamingEvents.Termination, _on_termination)
        self.client.on(
            StreamingEvents.Turn,
            lambda client, event: self._on_turn(client, event),
        )

        self.client.connect(
            StreamingParameters(
                sample_rate=sample_rate,
                format_turns=False,
            )
        )

    def _on_turn(self, client: StreamingClient, event: TurnEvent):
        text = (event.transcript or "").strip()
        if not text:
            return

        if event.end_of_turn:
            if self.on_final_callback:
                self.on_final_callback(text)

            if not event.turn_is_formatted:
                try:
                    client.set_params(StreamingSessionParameters(format_turns=True))
                except Exception as set_err:
                    print("set_params error:", set_err)
        else:
            if self.on_partial_callback:
                self.on_partial_callback(text)

    def stream_audio(self, audio_chunk: bytes):
        self.client.stream(audio_chunk)

    def close(self):
        self.client.disconnect(terminate=True)


def transcribe_audio(audio_file: UploadFile) -> str:
    """Transcribes audio to text using AssemblyAI."""
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file.file)

    if transcript.status == aai.TranscriptStatus.error or not transcript.text:
        raise Exception(f"Transcription failed: {transcript.error or 'No speech detected'}")

    return transcript.text