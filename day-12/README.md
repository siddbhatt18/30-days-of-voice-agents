# Day 12: Revamping the User Interface

Welcome to Day 12 of the 30 Days of Voice Agents Challenge\! Today, we've given our conversational agent a fresh, modern, and more intuitive user interface. The focus has been on streamlining the user experience and making the interaction feel more natural and engaging.

## 🧠 What We Built

  - **Simplified UI**: Removed the initial text-to-speech and echo bot sections to focus solely on the conversational agent. The interface is now cleaner and more centered on the primary task.
  - **Combined Record Button**: The "Start Recording" and "Stop Recording" buttons have been merged into a single, intelligent button that changes its appearance and functionality based on the application's state.
  - **Engaging Animations**: The record button now features a pulsing animation while recording, providing clear visual feedback to the user.
  - **Hidden Audio Player**: The audio player is now hidden by default and only appears when the agent is speaking, reducing visual clutter.
  - **Improved Styling**: The overall design has been revamped with a more modern aesthetic, including a card-based layout, shadows, and a more prominent record button.

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
    cd day-12/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-12/` directory and add your API keys:
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
day-12/
├── main.py           # Unchanged from Day 11
├── templates/
│   └── index.html    # Updated with the new, revamped UI
├── static/
│   ├── script.js     # Client-side logic for the new single-button interaction
│   └── fallback.mp3  # Unchanged
├── requirements.txt  # Unchanged
└── .env              # Unchanged
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
  - **Day 12**: Revamped the UI for a more streamlined and engaging user experience.
