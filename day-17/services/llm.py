# services/llm.py

import google.generativeai as genai
import os
from typing import List, Dict, Any, Tuple

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