# Day 10: Building a Conversational Agent with Chat History

Welcome to Day 10 of the 30 Days of Voice Agents Challenge\! Today, our voice agent gets a memory. We've implemented a chat history feature, allowing for more natural, context-aware conversations. The agent now remembers previous turns in the dialogue, making it a true conversational partner.

## 🧠 What We Built

  - **Chat History**: The agent now maintains a history of the conversation. When you speak, your transcribed message is added to the history, and the entire conversation context is sent to the LLM. This allows the agent to understand follow-up questions and references to earlier topics.
  - **Session Management**: A new endpoint, `POST /agent/chat/{session_id}`, has been created. A unique `session_id` is generated on the client-side and appended to the URL as a query parameter. This ID is used to associate each user with their specific conversation history on the server.
  - **In-Memory Datastore**: For simplicity and rapid prototyping, the chat history is stored in a Python dictionary on the server. Each `session_id` maps to a list of messages exchanged during that session.
  - **Continuous Conversation Flow**: The user interface has been updated to automatically start recording after the agent's audio response has finished playing. This creates a seamless, back-and-forth conversational experience.

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
    cd day-10/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the `day-10/` directory and add your API keys:
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
day-10/
├── main.py           # Updated with the new /agent/chat/{session_id} endpoint and in-memory history
├── templates/
│   └── index.html    # UI for the new conversational agent with history
├── static/
│   └── script.js     # Client-side logic for session management and continuous conversation
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
  - **Day 10**: Implemented chat history for context-aware conversations.
