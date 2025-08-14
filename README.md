Welcome to the 30 Days of Voice Agents Challenge\! This repository documents my journey of building voice-powered applications over 30 days. This project is a hands-on experience with various AI APIs, backend development with FastAPI, and frontend interactions using vanilla JavaScript.

-----

## 🤖 About The Project

This project is a fully-functional voice-based conversational AI agent. You can engage in a continuous, voice-to-voice conversation with an AI powered by Google's Gemini LLM. The agent remembers the context of your conversation, allowing for natural follow-up questions and a more human-like interaction.

### Features

  * **Voice-to-Voice Interaction**: Speak to the agent and receive a spoken response.
  * **Contextual Conversations**: The agent maintains a chat history for each session, enabling it to understand context and follow-ups.
  * **API Integration**: Seamlessly integrates multiple AI services for a complete STT → LLM → TTS pipeline.
  * **User-Friendly Interface**: A clean and modern UI with a single button for interaction and visual feedback for different states (ready, recording, thinking).
  * **Error Handling**: Includes a fallback audio response for graceful failure when an API call is unsuccessful.

-----

## 🛠️ Tech Stack

The application is built using a combination of Python for the backend, plain HTML/CSS/JavaScript for the frontend, and various AI APIs for the core functionalities.

  * **Backend**:
      * **FastAPI**: For building the robust and fast API server.
      * **Uvicorn**: As the ASGI server to run the FastAPI application.
      * **Python-Dotenv**: To manage environment variables for API keys.
  * **Frontend**:
      * **HTML, CSS, JavaScript**: For the structure, styling, and interactivity of the web interface.
      * **Bootstrap**: For responsive UI components.
      * **MediaRecorder API**: To capture audio directly from the user's microphone in the browser.
  * **AI & Voice APIs**:
      * **Murf AI**: For high-quality Text-to-Speech (TTS) synthesis.
      * **AssemblyAI**: For accurate Speech-to-Text (STT) transcription.
      * **Google Gemini**: As the Large Language Model (LLM) for generating intelligent responses.

-----

## ⚙️ Architecture

The application follows a client-server architecture. The frontend, running in the user's browser, captures audio and sends it to the backend. The FastAPI backend then orchestrates the communication between the three different AI APIs to generate a response.

Here is the flow for a single turn in a conversation:

1.  The **client** captures the user's voice and sends the audio file to the `/agent/chat/{session_id}` endpoint on the server.
2.  The **FastAPI server** receives the audio.
3.  It sends the audio to **AssemblyAI** for transcription (STT).
4.  The transcribed text is then sent to the **Google Gemini LLM**, along with the chat history for the current session.
5.  Gemini returns a text response, which the server then sends to **Murf AI** for speech synthesis (TTS).
6.  The server receives the final audio URL from Murf AI and sends it back to the client.
7.  The **client** plays the received audio, and the cycle continues.

-----

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

  * Python 3.8+
  * An IDE of your choice (e.g., VS Code)
  * API keys for Murf AI, AssemblyAI, and Google Gemini.

### Installation & Running the App

1.  **Clone the repo**
    ```sh
    git clone https://github.com/siddbhatt18/30-days-of-voice-agents.git
    ```
2.  **Navigate to the project directory** for Day 13:
    ```sh
    cd 30-days-of-voice-agents/day-13/
    ```
3.  **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the `day-13/` directory and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
5.  **Run the FastAPI server**:
    ```sh
    uvicorn main:app --reload
    ```
6.  **Open your browser** and visit `http://localhost:8000`. Grant microphone permissions if prompted.

-----

## ✅ Completed Days

  * **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
  * **Day 02**: Created a `/tts` endpoint for Text-to-Speech using Murf AI.
  * **Day 03**: Built a client-side interface for the TTS endpoint.
  * **Day 04**: Added a client-side echo bot using the `MediaRecorder` API.
  * **Day 05**: Implemented server-side audio upload.
  * **Day 06**: Added Speech-to-Text transcription with AssemblyAI.
  * **Day 07**: Created a voice-transforming echo bot.
  * **Day 08**: Integrated the Gemini LLM for intelligent text generation.
  * **Day 09**: Built a full voice-to-voice conversational agent.
  * **Day 10**: Implemented chat history for context-aware conversations.
  * **Day 11**: Added robust error handling and a fallback audio response.
  * **Day 12**: Revamped the UI for a more streamlined and engaging user experience.
  * **Day 13**: Created this comprehensive README file for the project.
