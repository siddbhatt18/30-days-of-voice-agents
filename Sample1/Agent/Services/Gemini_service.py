import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

my_api_key = os.getenv(
    "GEMINI_API_KEY")
genai.configure(api_key=my_api_key)


def get_response_from_gemini(conversation_history: list) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        messages = [
            {"role": "user" if msg["role"] ==
                "user" else "model", "parts": [msg["text"]]}
            for msg in conversation_history
        ]
        response = model.generate_content(messages)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "Sorry, I couldn't process that."
