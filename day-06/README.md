# Day 06: Speech-to-Text Transcription

Welcome to Day 6 of the 30 Days of Voice Agents Challenge\! Today, we're adding a crucial component to our application: the ability to understand and transcribe spoken words using **AssemblyAI**.

## 🧠 What We Built

  - **New Transcription Endpoint**: Created a `/transcribe/file` endpoint on our FastAPI server.
  - **AssemblyAI Integration**: The new endpoint takes an audio file and uses the AssemblyAI Python SDK to get a text transcription.
  - **UI Integration**: The frontend now sends the audio recorded via the `MediaRecorder` API directly to our new `/transcribe/file` endpoint.
  - **Display Transcription**: The UI has been updated to show a "Transcribing..." status and then displays the final text received from the server.
  - **No More Saving Files**: The server now processes the audio data in memory for transcription without needing to save it to a folder.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`, **`assemblyai`**
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API
  - **Voice APIs**: Murf AI (TTS), **AssemblyAI (STT)**

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-06/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-06/` directory and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000). You will need to grant microphone permissions.

## 📂 Project Structure

```
day-06/
├── main.py           # Updated with the new /transcribe/file endpoint
├── templates/
│   └── index.html    # Updated with UI for transcription results
├── static/
│   └── script.js     # Updated to send audio for transcription
├── requirements.txt  # Updated with assemblyai
└── .env              # Now includes ASSEMBLYAI_API_KEY
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint to generate speech from text using Murf AI.
  - **Day 03**: Built a client-side interface to interact with the `/tts` endpoint.
  - **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
  - **Day 05**: Implemented server-side audio upload and status display.
  - **Day 06**: Added speech-to-text transcription using AssemblyAI.
