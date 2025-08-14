# Day 03: Interactive Text-to-Speech Client

Welcome to Day 3 of the 30 Days of Voice Agents Challenge\! Today, we're bringing our Text-to-Speech (TTS) service to life by building an interactive frontend. Now, you can type in text, click a button, and hear the generated audio right from your web browser.

## 🧠 What We Built

We've enhanced our web application to include:

  - A user-friendly interface with a text field and a submit button.
  - A dropdown menu to select different voices for the TTS generation.
  - Client-side JavaScript to send a request to our FastAPI backend's `/tts` endpoint.
  - An HTML `<audio>` element that plays the audio file received from the server.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`
  - **Voice API**: Murf AI

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-03/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-03/` directory and add your Murf API key:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000).

## 📂 Project Structure

```
day-03/
├── main.py           # Backend logic with /tts and /voices endpoints
├── templates/
│   └── index.html    # HTML page with text input, button, and audio player
├── static/
│   └── script.js     # JavaScript to handle form submission and audio playback
├── requirements.txt  # Project dependencies
└── .env              # To store your API key
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint to generate speech from text using Murf AI.
  - **Day 03**: Built a client-side interface to interact with the `/tts` endpoint and play the generated audio.
