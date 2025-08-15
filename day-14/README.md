# Day 14: Modular Code and Service-Oriented Architecture

Welcome to Day 14 of the 30 Days of Voice Agents Challenge\! Today, we've focused on refactoring our codebase into a more modular and service-oriented architecture. This improves organization, scalability, and maintainability as we continue to add more complex features to our voice agent.

## 🧠 What We Built

  - **Service-Oriented Structure**: We've broken down the core functionalities (STT, LLM, TTS) into their own dedicated service modules. This separation of concerns makes the code cleaner and easier to manage.
  - **Configuration Module**: A new `config.py` module now handles the loading and configuration of all API keys and clients, centralizing our setup process.
  - **Schema Definitions**: We've introduced a `schemas.py` file to define data structures using Pydantic, ensuring clear and validated data transfer within the application.
  - **Organized Project Layout**: The project has been restructured with `services`, `static`, and `templates` directories, creating a more logical and scalable file organization.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `python-dotenv`, `requests`, `jinja2`, `assemblyai`, `google-generativeai`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API
  - **AI APIs**:
      - Murf AI (Text-to-Speech)
      - AssemblyAI (Speech-to-Text)
      - Google Gemini (Large Language Model)

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-14/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-14/` directory and add your API keys:
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
day-14/
├── main.py           # Main FastAPI application logic
├── config.py         # API key loading and configuration
├── schemas.py        # Pydantic data schemas
├── services/
│   ├── __init__.py
│   ├── stt.py        # Speech-to-Text service module
│   ├── llm.py        # Language Model service module
│   └── tts.py        # Text-to-Speech service module
├── templates/
│   └── index.html
├── static/
│   ├── script.js
│   └── fallback.mp3
├── requirements.txt
└── .env
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
  - **Day 13**: (Assumed) Initial planning and setup for code refactoring.
  - **Day 14**: Refactored the codebase into a modular, service-oriented architecture.
