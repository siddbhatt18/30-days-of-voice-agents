# Day 18: Real-Time Transcription with Turn Detection

Welcome to Day 18 of the 30 Days of Voice Agents Challenge\! Today, we are enhancing our real-time transcription feature by implementing **turn detection** with AssemblyAI's streaming API. This will allow our voice agent to know when the user has finished speaking.

## 🧠 What We Built

  * **Turn Detection**: The server now leverages AssemblyAI's turn detection to identify when the user has stopped speaking.
  * **End-of-Turn Notifications**: A WebSocket message is sent from the server to the client to signify the end of a user's turn.
  * **UI Updates on Turn End**: The user interface is updated to display the final transcription only after a turn is completed, creating a more intuitive user experience.

-----

## 🛠 Tech Stack

The tech stack has been updated to incorporate AssemblyAI's turn detection feature.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai` (Streaming Client with Turn Detection), `google-generativeai`, `python-dotenv`, `websockets`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, **WebSocket API**
  * **AI APIs**:
      * Murf AI (Text-to-Speech)
      * **AssemblyAI (Real-Time Speech-to-Text with Turn Detection)**
      * Google Gemini (Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-18/
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

The main changes are in `main.py` to handle turn detection events and in `static/script.js` to process the end-of-turn messages.

```
day-18/
├── main.py           # Updated to handle AssemblyAI turn detection events
├── config.py
├── services/
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js     # Updated to display transcription at the end of a turn
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
