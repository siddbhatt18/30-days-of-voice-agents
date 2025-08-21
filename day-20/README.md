# Day 20: Streaming Text-to-Speech with Murf AI

Welcome to Day 20 of the 30 Days of Voice Agents Challenge\! Today, we're taking a huge leap forward in reducing latency by **streaming the LLM's text response directly to Murf AI for real-time Text-to-Speech (TTS) conversion**.

## 🧠 What We Built

  * **Real-Time Text-to-Speech**: Integrated Murf AI's WebSocket API to stream the Large Language Model's (LLM) response for immediate audio conversion as it's being generated.
  * **Streaming Audio Reception**: The server is now capable of receiving the synthesized audio from Murf AI as a continuous stream of base64 encoded audio chunks.
  * **Console Output for Audio Stream**: The incoming base64 audio chunks from Murf AI are printed to the server's console, providing real-time verification of the streaming TTS functionality.
  * **Efficient Context Management**: Implemented a static `context_id` for all Murf AI WebSocket requests. This ensures that a single TTS context is used throughout the session, preventing errors related to context limits.

-----

## 🛠 Tech Stack

The tech stack has been enhanced to support real-time, streaming Text-to-Speech.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai` (with streaming), `python-dotenv`, `websockets`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, `WebSocket API`
  * **AI APIs**:
      * **Murf AI (Streaming Text-to-Speech via WebSockets)**
      * AssemblyAI (Real-Time Speech-to-Text with Turn Detection)
      * Google Gemini (Streaming Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-20/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit `http://localhost:8000`. Grant microphone permissions if prompted.

-----

## 📂 Project Structure

The primary changes are within the `services/llm.py` file to handle the new integration with Murf AI's streaming TTS service.

```
day-20/
├── main.py
├── config.py
├── services/
│   └── llm.py        # Updated to stream LLM text to Murf AI via WebSockets
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js
├── requirements.txt
└── .env
```

-----

## ✅ Completed Days

  * **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  * **Day 02**: Created a `/tts` endpoint for Text-to-Speech using Murf AI.
  * **Day 03**: Built a client-side interface for the TTS endpoint.
  * **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
  * **Day 05**: Implemented server-side audio upload.
  * **Day 06**: Added Speech-to-Text transcription with AssemblyAI.
  * **Day 07**: Created a voice-transforming echo bot.
  * **Day 08**: Integrated the Gemini LLM for intelligent text generation.
  * **Day 09**: Built a full voice-to-voice conversational agent.
  * **Day 10**: Implemented chat history for context-aware conversations.
  * **Day 11**: Added robust error handling and a fallback audio response.
  * **Day 12**: Revamped the UI for a more streamlined and engaging user experience.
  * **Day 13**: Created the main project `README.md` file.
  * **Day 14**: Refactored the codebase into a modular, service-oriented architecture.
  * **Day 15**: Added a foundational WebSocket endpoint to the server.
  * **Day 16**: Implemented real-time audio streaming from the client using WebSockets.
  * **Day 17**: Added real-time transcription with AssemblyAI's Python SDK.
  * **Day 18**: Implemented turn detection with AssemblyAI to identify when the user has finished speaking.
  * **Day 19**: Implemented streaming of the LLM's response to the server console.
  * **Day 20**: Integrated real-time streaming Text-to-Speech with Murf AI.
