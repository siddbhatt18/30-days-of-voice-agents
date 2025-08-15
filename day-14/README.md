# Day 14: Integrating a Second TTS Provider (ElevenLabs)

Welcome to Day 14 of the 30 Days of Voice Agents Challenge\! To give our agent more personality and variety, today we've integrated a new Text-to-Speech (TTS) provider: **ElevenLabs**. Users can now choose from a selection of voices, including our original Murf AI voice and new options from ElevenLabs.

## 🧠 What We Built

  * **ElevenLabs Integration**: The backend has been enhanced to support **ElevenLabs** as a second TTS engine, providing access to a new range of high-quality voices.
  * **Dynamic Voice Selection**: The core `/agent/chat/{session_id}` endpoint now accepts a `voice_id` parameter. This allows the server to dynamically select the appropriate TTS provider and voice for synthesizing the agent's response.
  * **UI for Voice Choice**: The frontend has been updated with a simple set of radio buttons, enabling users to select their preferred voice before starting a conversation. The chosen voice is then passed to the backend with each request.
  * **Improved Configuration**: We've migrated from `python-dotenv` to **Pydantic's Settings Management** for a more robust, type-safe, and structured way of handling API keys and other configuration variables.

-----

## 🛠 Tech Stack

Our tech stack is expanding with more powerful tools for voice synthesis and configuration.

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
3.  **Create a `.env` file** and add your API keys. Note the new key for ElevenLabs.
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
5.  **Open your browser** and visit `http://localhost:8000`. You will now see options to select a voice before you start recording.

-----

## 📂 Project Structure

The project structure has been updated to accommodate the new TTS provider and UI changes.

```
day-14/
├── main.py           # Updated with ElevenLabs client, Pydantic settings, and dynamic TTS logic
├── templates/
│   └── index.html    # UI updated with voice selection radio buttons
├── static/
│   ├── script.js     # Client-side logic to pass the selected voice_id to the backend
│   └── fallback.mp3
├── requirements.txt  # Added elevenlabs and pydantic-settings
└── .env.example      # Example environment file with new keys
```

-----

## ✅ Completed Days

  * **Day 01 - 12**: From basic server setup to a fully conversational agent with a revamped UI and error handling.
  * **Day 13**: Created comprehensive project documentation (`README.md`).
  * **Day 14**: Integrated **ElevenLabs** as a second TTS provider with UI selection.
