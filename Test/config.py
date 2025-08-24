# config.py
import os
from dotenv import load_dotenv
import assemblyai as aai
import google.generativeai as genai
import logging

# Load environment variables from .env file
load_dotenv()

# Load API Keys from environment
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure APIs and log warnings if keys are missing
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY
else:
    logging.warning("ASSEMBLYAI_API_KEY not found in .env file.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logging.warning("GEMINI_API_KEY not found in .env file.")

if not MURF_API_KEY:
    logging.warning("MURF_API_KEY not found in .env file.")