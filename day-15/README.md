# Day 15: Introducing WebSockets for Real-Time Communication

Welcome to Day 15 of the 30 Days of Voice Agents Challenge\! Today, we're laying the groundwork for a faster, more interactive experience by adding **WebSocket support** to our backend. This is a foundational step towards enabling real-time, bidirectional communication between the client and the server.

## 🧠 What We Built

  * **New WebSocket Endpoint**: A new `/ws` endpoint has been added to the FastAPI application. This endpoint establishes a persistent, two-way communication channel with the client.
  * **Simple Echo Functionality**: For this initial implementation, the WebSocket serves as a basic echo test. When the server receives a text message through the connection, it sends a response back confirming the message was received (e.g., "Message text was: \[data]").
  * **Foundation for Future Streaming**: While the main chat functionality still uses the HTTP endpoint, this WebSocket is the first step toward enabling real-time audio streaming. This will eventually allow for faster transcription and more fluid, low-latency conversations with the agent.

-----

## 🛠 Tech Stack

The tech stack has been updated to include WebSockets, a key technology for real-time web applications.

  * **Backend**: `FastAPI`, `uvicorn`, `requests`, `assemblyai`, `google-generativeai`, `python-dotenv`, **WebSockets**
  * **Frontend**: `HTML`, `Bootstrap`, `JavaScript`, `MediaRecorder` API
  * **AI APIs**:
      * Murf AI (Text-to-Speech)
      * AssemblyAI (Speech-to-Text)
      * Google Gemini (Large Language Model)

-----

## 🚀 Run the App

The instructions to run the main application are unchanged. The WebSocket functionality is a backend addition and does not yet have a corresponding UI component.

1.  **Navigate to the project directory:**
    ```bash
    cd day-15/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit `http://localhost:8000`. The main chat agent will function as it did on Day 14.

-----

## 📂 Project Structure

The primary change in the project is the addition of the WebSocket endpoint in the main application file.

```
day-15/
├── main.py           # Updated with the new @app.websocket("/ws") endpoint
├── config.py
├── services/
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   └── script.js
├── requirements.txt
└── .env
```

-----

## ✅ Completed Days

  * **Day 01 - 14**: From basic server setup to a fully documented, refactored conversational agent.
  * **Day 15**: Added a foundational **WebSocket endpoint** to the server for future real-time communication.
