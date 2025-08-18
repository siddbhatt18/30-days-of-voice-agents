# Day 17: Real-Time Transcription with AssemblyAI

Welcome to Day 17 of the 30 Days of Voice Agents Challenge\! Today, we're building upon our real-time audio streaming foundation by integrating **AssemblyAI's Python SDK to perform real-time transcription**.

## 🧠 What We Built

  * **Real-Time Transcription**: The server now uses AssemblyAI's streaming transcription client to get live transcripts of the audio being streamed from the client.
  * **WebSocket Communication for Transcripts**: The server sends the received transcripts back to the client over the same WebSocket connection.
  * **Live UI Updates**: The frontend JavaScript code receives the transcription data and dynamically updates the UI to display the live transcript to the user as they speak.
  * **Console Output**: The transcript is also printed to the Python server's console for debugging and real-time monitoring.

-----

## 🛠 Tech Stack

The tech stack has been updated to include AssemblyAI's streaming client for real-time transcription.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, **`assemblyai` (Streaming Client)**, `google-generativeai`, `python-dotenv`, `websockets`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, **WebSocket API**
  * **AI APIs**:
      * Murf AI (Text-to-Speech)
      * **AssemblyAI (Real-Time Speech-to-Text)**
      * Google Gemini (Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-17/
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

The main changes are in `main.py` to integrate the AssemblyAI streaming client and in `static/script.js` to handle the incoming transcription messages.

```
day-17/
├── main.py           # Updated with AssemblyAI streaming transcription logic
├── config.py
├── services/
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js     # Updated to display live transcription
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
