# Day 09: Full Voice-to-Voice LLM Conversation

Welcome to Day 9 of the 30 Days of Voice Agents Challenge\! Today, we've transformed our application into a true voice-to-voice conversational agent. Now, you can speak a question and receive a spoken answer, creating a seamless, hands-free interaction.

## 🧠 What We Built

  - **End-to-End Voice Pipeline**: The `/llm/query` endpoint now orchestrates a complete voice-in, voice-out workflow:
    1.  **Voice Input**: The server accepts an audio file as input.
    2.  **Speech-to-Text**: The incoming audio is transcribed to text using the **AssemblyAI API**.
    3.  **LLM Processing**: The transcribed text is sent as a prompt to the **Google Gemini API** to generate an intelligent response.
    4.  **Text-to-Speech**: The LLM's text response is then synthesized back into audio using the **Murf AI API**.
    5.  **Voice Output**: The final audio URL is sent back to the client for playback.
  - **Interactive UI**: The frontend is now fully geared for voice interaction. Clicking "Start Recording" captures your question, and the agent's spoken response is played back automatically.
  - **Status Updates**: The UI provides real-time feedback, letting you know when it's "Recording...", "Thinking...", and when it's ready to play the response.

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
    cd day-09/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-09/` directory and add your API keys:
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
day-09/
├── main.py           # Updated with the full voice-to-voice /llm/query endpoint
├── templates/
│   └── index.html    # UI for the new conversational agent
├── static/
│   └── script.js     # Client-side logic for recording and handling the voice conversation
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
