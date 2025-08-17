# Day 16: Real-Time Audio Streaming with WebSockets

Welcome to Day 16 of the 30 Days of Voice Agents Challenge\! Today, we're taking a major step towards a more responsive and fluid user experience by implementing **real-time audio streaming** from the client to the server using WebSockets.

## 🧠 What We Built

  * **Client-Side Streaming**: The JavaScript client now captures audio from the microphone and streams it to the server in real-time over a WebSocket connection as soon as the user starts speaking.
  * **WebSocket Integration**: The `/ws` endpoint on our FastAPI server is now fully integrated to receive and handle incoming audio data chunks.
  * **Continuous Audio Processing**: The server can now process audio as it arrives, laying the foundation for real-time transcription and more immediate responses from our voice agent.
  * **Enhanced User Interaction**: This moves us away from a "record-then-send" model to a more natural, continuous "speak-and-process" interaction, significantly reducing perceived latency.

-----

## 🛠 Tech Stack

The tech stack has been updated to fully leverage WebSockets for real-time data transfer.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai`, `python-dotenv`, **WebSockets**
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, **WebSocket API**
  * **AI APIs**:
      * Murf AI (Text-to-Speech)
      * AssemblyAI (Speech-to-Text)
      * Google Gemini (Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-16/
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

The main changes are in the client-side JavaScript, which now includes the logic for streaming audio over a WebSocket.

```
day-16/
├── main.py           # Updated to handle incoming WebSocket audio streams
├── config.py
├── services/
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js     # Updated with WebSocket audio streaming logic
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
