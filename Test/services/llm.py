# services/llm.py

import google.generativeai as genai
import websockets
import json
import asyncio
import re
import logging
import os
from typing import List, Dict, Any, Tuple

# Configure logging
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in .env file.")

if not MURF_API_KEY:
    print("Warning: MURF_API_KEY not found in .env file.")

def get_llm_response(user_query: str, history: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Gets a response from the Gemini LLM and updates chat history."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=history)
    response = chat.send_message(user_query)
    return response.text, chat.history

async def receive_loop(ws):
    """Receive audio chunks from Murf WebSocket"""
    audio_chunks = []
    chunk_count = 1
    try:
        while True:
            response = await ws.recv()
            data = json.loads(response)
            
            if "audio" in data and data["audio"]:
                base64_chunk = data["audio"]
                max_len = 64
                if len(base64_chunk) > max_len:
                    truncated_chunk = f"{base64_chunk[:30]}...{base64_chunk[-30:]}"
                else:
                    truncated_chunk = base64_chunk
                print(f"[murf ai][chunk {chunk_count}] {truncated_chunk}")
                audio_chunks.append(base64_chunk)
                chunk_count += 1
            
            if data.get("final"):
                logger.info("Murf confirms final audio chunk received.")
                break
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        logger.error(f"Error in receive loop: {str(e)}")
    return audio_chunks

def get_llm_streaming_response(user_query: str, history: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Gets a streaming response from the Gemini LLM, accumulates it, and returns final response with history."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=history)
    
    # Generate streaming response
    response = chat.send_message(user_query, stream=True)
    
    # Accumulate the streaming response and print to console
    accumulated_response = ""
    
    # Process each chunk from the streaming response
    for chunk in response:
        if chunk.text:
            accumulated_response += chunk.text
            print(chunk.text, end="", flush=True)  # Print each chunk as it arrives
    
    return accumulated_response, chat.history

async def get_llm_streaming_response_with_murf(user_query: str, history: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]], List[str]]:
    """
    Gets a streaming response from Gemini LLM, sends sentences to Murf via WebSocket,
    and returns the text response, updated history, and audio chunks.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is missing.")
    if not MURF_API_KEY:
        raise ValueError("Murf API key is missing.")
    
    context_id = "day20-static-context"  # Static context_id for Murf to avoid context limit errors
    
    try:
        # Connect to Murf WebSocket
        uri = (
            f"wss://api.murf.ai/v1/speech/stream-input"
            f"?api-key={MURF_API_KEY}"
            f"&sample_rate=44100"
            f"&channel_type=MONO"
            f"&format=WAV"
        )
        
        async with websockets.connect(uri) as ws:
            # Send voice configuration
            voice_config = {
                "context_id": context_id,
                "voice_config": {
                    "voiceId": "en-US-darnell",
                    "style": "Conversational"
                }
            }
            await ws.send(json.dumps(voice_config))
            
            # Start the audio receiver task
            receiver_task = asyncio.create_task(receive_loop(ws))
            
            # Generate streaming response from Gemini
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=history)
            stream = chat.send_message(user_query, stream=True)
            
            sentence_buffer = ""
            accumulated_response = ""
            
            print("\nGEMINI STREAMING RESPONSE \n")
            for chunk in stream:
                if chunk.text:
                    accumulated_response += chunk.text
                    sentence_buffer += chunk.text
                    print(chunk.text, end="", flush=True)

                    # Split into sentences using regex
                    sentences = re.split(r'(?<=[.?!])\s+', sentence_buffer)

                    if len(sentences) > 1:
                        # Send complete sentences to Murf
                        for sentence in sentences[:-1]:
                            if sentence.strip():
                                text_msg = {
                                    "context_id": context_id,
                                    "text": sentence.strip(),
                                    "end": False
                                }
                                await ws.send(json.dumps(text_msg))
                        sentence_buffer = sentences[-1]

            # Send final sentence buffer if any
            if sentence_buffer.strip():
                text_msg = {
                    "context_id": context_id,
                    "text": sentence_buffer.strip(),
                    "end": True
                }
                await ws.send(json.dumps(text_msg))

            print("\nEND OF GEMINI STREAM\n")

            # Wait for all audio chunks from Murf
            audio_chunks = await receiver_task

            if not accumulated_response:
                raise ValueError("No response from Gemini LLM stream.")

            return accumulated_response, chat.history, audio_chunks

    except genai.types.generation_types.BlockedPromptException as e:
        logger.error(f"Gemini blocked prompt: {str(e)}")
        raise
    except genai.types.generation_types.StopCandidateException as e:
        logger.error(f"Gemini stopped generation: {str(e)}")
        raise
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Murf WebSocket closed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise