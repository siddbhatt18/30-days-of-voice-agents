# Day 21: Streaming Audio to the Client

Welcome to Day 21 of the 30 Days of Voice Agents Challenge\! Today, we're completing the real-time loop by **streaming the synthesized audio from the server directly to the client** over WebSockets.

## 🧠 What We Built

  * **End-to-End Audio Streaming**: The base64 encoded audio chunks received from Murf AI are now streamed in real-time from our FastAPI server to the client's browser.
  * **Client-Side Audio Assembly**: The frontend JavaScript code has been updated to receive the incoming audio chunks and accumulate them into an array, preparing them for playback.
  * **Real-Time Acknowledgement**: The client now sends an acknowledgement back to the server for each audio chunk it receives, which is printed on the client's browser console for verification.
  * **Full Conversational Loop**: This step completes the entire streaming pipeline: the user speaks, the audio is transcribed in real-time, the transcription is sent to a streaming LLM, the LLM's text response is streamed to a TTS service, and the resulting audio is streamed back to the client.

-----

## 🛠 Tech Stack

The tech stack remains consistent, with a focus on real-time communication between the client and server.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai` (with streaming), `python-dotenv`, `websockets`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, `WebSocket API`
  * **AI APIs**:
      * Murf AI (Streaming Text-to-Speech via WebSockets)
      * AssemblyAI (Real-Time Speech-to-Text with Turn Detection)
      * Google Gemini (Streaming Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-21/
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

The main changes are in `main.py` to send audio chunks and `static/script.js` to receive them.

```
day-21/
├── main.py           # Updated to stream audio chunks to the client
├── config.py
├── services/
│   └── llm.py
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js     # Updated to receive and acknowledge audio chunks
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
  * **Day 21**: Implemented streaming of synthesized audio to the client.
