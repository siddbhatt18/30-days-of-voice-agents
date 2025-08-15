# Day 14: Code Refactoring & ElevenLabs Integration

Welcome to Day 14 of the 30 Days of Voice Agents Challenge\! Today's focus was on improving the project's foundation by refactoring the code for better maintainability and adding **ElevenLabs** as a second Text-to-Speech (TTS) provider, giving users more voice options.

## 🧠 What We Built

  * **Major Code Refactoring**: The backend code has been significantly reorganized. The logic for interacting with external AI services (AssemblyAI, Gemini, Murf, ElevenLabs) has been extracted from `main.py` and moved into a dedicated `services` directory. This makes the code cleaner, more modular, and easier to manage.
  * **ElevenLabs Integration**: We've added support for **ElevenLabs**, a popular and high-quality voice synthesis service. The agent can now generate responses using either Murf AI or ElevenLabs.
  * **UI for Voice Selection**: The frontend has been updated with radio buttons, allowing the user to choose their preferred voice before starting the conversation.
  * **Structured Configuration and Schemas**:
      * A `config.py` file using **Pydantic Settings** has been introduced for a more robust and type-safe way of managing environment variables and API keys.
      * A `schemas.py` file now defines Pydantic models for our data, ensuring better data validation and consistency.

-----

## 🛠 Tech Stack

Our tech stack has been updated with new libraries for voice synthesis and configuration management.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai`, **`elevenlabs`**, **`pydantic-settings`**
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API
  * **AI APIs**:
      * **Murf AI** & **ElevenLabs** (Text-to-Speech)
      * **AssemblyAI** (Speech-to-Text)
      * **Google Gemini** (Large Language Model)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-14/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-14/` directory. You now need to add your ElevenLabs API key.
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit `http://localhost:8000`. You will now see options to select a voice before recording.

-----

## 📂 Project Structure

The project has been refactored into a more scalable and organized structure.

```
day-14/
├── main.py           # Slimmed down to handle routing and core logic
├── config.py         # New file for Pydantic settings management
├── schemas.py        # New file for Pydantic data models
├── services/         # New directory for external API services
│   ├── stt.py
│   ├── llm.py
│   └── tts.py
├── templates/
│   └── index.html    # Updated with voice selection UI
├── static/
│   └── script.js     # Updated to send the selected voice
├── requirements.txt  # Added elevenlabs and pydantic-settings
└── .env
```

-----

## ✅ Completed Days

  * **Day 01 - 12**: Journey from a basic server to a fully functional voice agent with chat history and a polished UI.
  * **Day 13**: Created comprehensive project documentation.
  * **Day 14**: Refactored the codebase and integrated **ElevenLabs** as a second TTS provider.
