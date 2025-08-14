# Day 08: Integrating a Large Language Model (LLM)

Welcome to Day 8 of the 30 Days of Voice Agents Challenge\! Today marks a significant milestone as we introduce a Large Language Model (LLM) into our backend. We're using **Google's Gemini API** to give our application the ability to generate intelligent, human-like responses to text queries.

## 🧠 What We Built

  - **New LLM Endpoint**: We've added a new `POST /llm/query` endpoint to our FastAPI server.
  - **Gemini API Integration**: This endpoint takes a text string as input, sends it to the Gemini API, and receives a generated response.
  - **Text-Based Interaction**: For now, the interaction is purely text-based. The server receives text and returns text, laying the groundwork for future voice-to-voice conversations.
  - **No UI Changes**: As this is a backend-focused task, the user interface remains the same as in Day 7. The new endpoint can be tested using API documentation tools like FastAPI's built-in Swagger UI.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`, `assemblyai`, **`google-generativeai`**
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`
  - **AI APIs**:
      - Murf AI (Text-to-Speech)
      - AssemblyAI (Speech-to-Text)
      - **Google Gemini** (Large Language Model)

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-08/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-08/` directory and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Test the new endpoint** by visiting the API documentation at [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs).

## 📂 Project Structure

```
day-08/
├── main.py           # Updated with the new /llm/query endpoint and Gemini integration
├── templates/
│   └── index.html    # Unchanged from Day 7
├── static/
│   └── script.js     # Unchanged from Day 7
├── requirements.txt  # Updated with google-generativeai
└── .env              # Now includes GEMINI_API_KEY
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
