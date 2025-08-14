# Day 04: Building a Client-Side Echo Bot

Welcome to Day 4 of the 30 Days of Voice Agents Challenge\! Today's task is to add a client-side "Echo Bot" to our web page. This feature uses the browser's built-in capabilities to record audio from a microphone and play it back, all without involving the server.

## 🧠 What We Built

  - **A new "Echo Bot" UI section** added to our existing HTML page.
  - **Microphone Recording**: Implemented audio recording directly in the browser using the `MediaRecorder` API.
  - **Recording Controls**: Added "Start Recording" and "Stop Recording" buttons to control the recording process.
  - **Instant Playback**: The recorded audio is immediately playable on the page using an HTML `<audio>` element.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn` (No changes from Day 3)
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, **`MediaRecorder` API**

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-04/
    ```
2.  **Install the required dependencies** (if you haven't already):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
4.  **Open your browser** and visit [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000). You will likely need to grant the page permission to access your microphone.

## 📂 Project Structure

```
day-04/
├── main.py           # Unchanged from Day 3
├── templates/
│   └── index.html    # Updated with the new Echo Bot section
├── static/
│   └── script.js     # Updated with MediaRecorder logic
├── requirements.txt  # Unchanged
└── .env              # Unchanged
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint to generate speech from text using Murf AI.
  - **Day 03**: Built a client-side interface to interact with the `/tts` endpoint.
  - **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
