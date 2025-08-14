# Day 11: Robust Error Handling and Fallbacks

Welcome to Day 11 of the 30 Days of Voice Agents Challenge\! Today, we're making our conversational agent more resilient. Real-world applications need to handle unexpected issues gracefully, so we've added robust error handling on both the server and the client to manage API failures and other problems.

## 🧠 What We Built

  - **Server-Side Error Handling**: The `/agent/chat/{session_id}` endpoint in our FastAPI server is now wrapped in a comprehensive `try-except` block. This allows it to catch any exceptions that occur during the STT, LLM, or TTS API calls.
  - **Fallback Audio Response**: If any of the external APIs fail, the server now sends a pre-recorded fallback audio message ("I'm having trouble connecting right now") instead of a JSON error. This provides a more user-friendly experience.
  - **Client-Side Error Detection**: The client-side JavaScript has been updated to check for a special `X-Error` header in the server's response. This header indicates that the fallback audio is being sent, allowing the client to handle it appropriately.
  - **Graceful Failure**: When an error is detected, the client plays the fallback audio and re-enables the recording button, allowing the user to try their request again without needing to refresh the page.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`, `assemblyai`, `google-generativeai`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API
  - **AI APIs**:
      - Murf AI (Text-to-Speech)
      - AssemblyAI (Speech-to-Text)
      - Google Gemini (Large Language Model)

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-11/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-11/` directory and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit http://localhost:8000. Grant microphone permissions if prompted.

## 📂 Project Structure

```
day-11/
├── main.py           # Updated with try-except blocks and fallback audio response
├── templates/
│   └── index.html    # UI for the conversational agent
├── static/
│   ├── script.js     # Client-side logic for handling errors
│   └── fallback.mp3  # New fallback audio file
├── requirements.txt  # Project dependencies
└── .env              # To store your API keys
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint for Text-to-Speech using Murf AI.
  - **Day 03**: Built a client-side interface for the TTS endpoint.
  - **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
  - **Day 05**: Implemented server-side audio upload.
  - **Day 06**: Added Speech-to-Text transcription with AssemblyAI.
  - **Day 07**: Created a voice-transforming echo bot.
  - **Day 08**: Integrated the Gemini LLM for intelligent text generation.
  - **Day 09**: Built a full voice-to-voice conversational agent.
  - **Day 10**: Implemented chat history for context-aware conversations.
  - **Day 11**: Added robust error handling and a fallback audio response.
