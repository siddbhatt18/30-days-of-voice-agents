# services/llm.py

import google.generativeai as genai
import os
from typing import List, Dict, Any, Tuple, Generator

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in .env file.")

def get_llm_response(user_query: str, history: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Gets a response from the Gemini LLM and updates chat history."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=history)
    response = chat.send_message(user_query)
    return response.text, chat.history

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