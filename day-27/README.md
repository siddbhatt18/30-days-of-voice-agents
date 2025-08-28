# Day 27: UI-Based Configuration and Code Refactoring

Welcome to Day 27 of the 30 Days of Voice Agents Challenge\! Today, we've focused on massively improving the user experience by revamping the UI and adding a settings panel to configure API keys directly in the browser.

## 🧠 What We Built

  * **API Key Configuration via UI**: We've removed the dependency on the `.env` file for runtime configuration. Now, you can enter your API keys for Murf, AssemblyAI, Gemini, and SerpAPI through a settings modal in the UI. These keys are securely stored in your browser's local storage.
  * **Complete UI Revamp**: The user interface has been redesigned for a cleaner, more modern, and more intuitive user experience.
  * **Code Cleanup and Refactoring**: The backend code was significantly refactored. The `config.py` file has been removed, and services are now decoupled from a global configuration, making the code cleaner and more modular.

-----

## 🛠 Tech Stack

The tech stack remains the same, but the way we handle configuration has been completely overhauled.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai`, `python-dotenv`, `websockets`, `google-search-results`
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript` (with `AudioContext` and `WebSocket API`), `MediaRecorder` API
  * **AI APIs**:
      * Murf AI (Streaming Text-to-Speech)
      * AssemblyAI (Real-Time Speech-to-Text with Turn Detection)
      * Google Gemini (Streaming LLM with Function Calling)
      * SerpAPI (Real-time Google Search Results)

-----

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd "AI Voice Agent"
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
4.  **Open your browser** and visit `http://localhost:8000`.
5.  **Click the settings icon** in the top-right corner to enter and save your API keys. Grant microphone permissions and start chatting\!

-----

## 📂 Project Structure

The project structure has been simplified by removing the `config.py` file.

```
AI Voice Agent/
├── main.py      # Updated to handle API keys from the client
├── services/
│   ├── llm.py   # Refactored to accept API keys as arguments
│   ├── stt.py   # Refactored to accept API keys as arguments
│   └── tts.py   # Refactored to accept API keys as arguments
├── schemas.py
├── templates/
│   └── index.html # Updated with the new settings modal
├── static/
│   ├── script.js  # Handles API key storage and UI logic
│   └── style.css  # Updated styles for the new UI
├── requirements.txt
└── .env           # No longer used for runtime config
```

-----

## ✅ Completed Days

  * **Day 01 - 24**: Foundational work from setting up the server to giving the agent a persona.
  * **Day 25**: Equipped the agent with a web search skill using a tool-use paradigm.
  * **Day 26**: Made the web search skill intelligent by adding automatic detection for when it's needed.
  * **Day 27**: Revamped the UI and implemented a settings panel for API key configuration.
