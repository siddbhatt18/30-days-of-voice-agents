# Day 05: Server-Side Audio Upload

Welcome to Day 5 of the 30 Days of Voice Agents Challenge\! Today, we're taking our echo bot to the next level by sending the recorded audio to our Python server. This bridges the gap between the client-side recording and server-side processing.

## 🧠 What We Built

  - **Audio Upload Functionality**: The client now uploads the recorded audio to the server as soon as the recording stops.
  - **New Server Endpoint**: A new `/upload-audio` endpoint on the FastAPI server that receives the audio file.
  - **File Storage**: The server saves the uploaded audio file temporarily into a local `/uploads` directory.
  - **UI Status Updates**: The user interface now displays the status of the upload (e.g., "Uploading...", "Upload Successful\!").
  - **Server Response**: The server sends back a JSON response containing the uploaded file's name, content type, and size, which is then displayed on the UI.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-multipart`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-05/
    ```
2.  **Install the required dependencies** (if you haven't already):
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-05/` directory and add your Murf API key (if not already done):
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000). Grant microphone permissions if prompted.

## 📂 Project Structure

```
day-05/
├── main.py           # Updated with the new /upload-audio endpoint
├── uploads/          # New folder to temporarily store audio
├── templates/
│   └── index.html    # Updated with UI for upload status
├── static/
│   └── script.js     # Updated to send audio to the server
├── requirements.txt  # Updated with python-multipart
└── .env              # Unchanged
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint to generate speech from text using Murf AI.
  - **Day 03**: Built a client-side interface to interact with the `/tts` endpoint.
  - **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
  - **Day 05**: Implemented server-side audio upload and status display.
