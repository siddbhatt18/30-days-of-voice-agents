# Day 19: Streaming LLM Responses

Welcome to Day 19 of the 30 Days of Voice Agents Challenge\! Today, we're making our voice agent even more responsive by **streaming the Large Language Model's (LLM) response** back to the server.

## 🧠 What We Built

  * **Streaming LLM Integration**: Once the final transcription is received from AssemblyAI, it is immediately sent to the LLM API to generate a response.
  * **Real-Time Response Generation**: The server is now able to receive the LLM's response as a stream of text chunks.
  * **Console Output for Streaming Response**: The incoming text chunks from the LLM are accumulated and printed to the server's console in real-time, allowing us to see the response as it's being generated.
  * **Preparation for Streaming to Client**: This lays the groundwork for sending the LLM's response to the client in real-time in a future step.

-----

## 🛠 Tech Stack

The tech stack has been updated to handle streaming responses from the LLM.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, **`google-generativeai` (with streaming)**, `python-dotenv`, `websockets`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API, `WebSocket API`
  * **AI APIs**:
      * Murf AI (Text-to-Speech)
      * AssemblyAI (Real-Time Speech-to-Text with Turn Detection)
      * **Google Gemini (Streaming Large Language Model)**

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-19/
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

The main changes are in the `services/llm.py` file to handle the streaming response from the LLM.

```
day-19/
├── main.py
├── config.py
├── services/
│   └── llm.py        # Updated to handle streaming LLM responses
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
