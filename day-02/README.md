# Day 02: Text-to-Speech with Murf AI

Welcome to Day 2 of the 30 Days of Voice Agents Challenge\! Today, we're building on our FastAPI server by adding a Text-to-Speech (TTS) endpoint that integrates with the **Murf AI API**.

## 🧠 What We Built

A FastAPI server with a new `/tts` endpoint that:

  - Accepts a text string as input.
  - Calls the Murf AI `/speech/generate` REST API to convert the text into speech.
  - Returns a JSON response containing a URL to the generated audio file.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`
  - **Voice API**: Murf AI

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-02/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-02/` directory and add your Murf API key:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs) to access the API documentation and test the endpoint.

## 🧪 Testing the Endpoint

You can test the new `/tts` endpoint using FastAPI's interactive documentation:

1.  Go to [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs).
2.  Expand the `POST /tts` endpoint.
3.  Click "**Try it out**".
4.  Enter some text in the `text` field.
5.  Click "**Execute**".

You'll see the server's response, which will include the `audio_url` of the generated speech.

## 📂 Project Structure

```
day-02/
├── main.py           # Backend logic with the new /tts endpoint
├── templates/
│   └── index.html    # Basic HTML file (unchanged from Day 1)
├── static/
│   └── script.js     # Basic JavaScript (unchanged from Day 1)
├── requirements.txt  # Project dependencies
└── .env              # To store your API key
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  - **Day 02**: Created a `/tts` endpoint to generate speech from text using Murf AI.
