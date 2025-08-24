# 🎙️ Murf AI Voice Agent Challenge

Welcome to my journey through the **Murf AI Voice Agent 30-Day Challenge**!
I'm building a smart and interactive **voice agent** using Murf AI's powerful TTS capabilities and integrating it with real-time tech like **AssemblyAI, FastAPI**, and **LLM APIs**.

---

### 🗓️ Day 1 – Kickoff & Setup

- 🚀 Joined the **Murf AI Voice Agent Challenge**
- 🧠 Explored the challenge format, goals, and tools
- 💻 Set up the base project using **FastAPI**
- 🔐 Registered and tested the **Murf API key**
- 🎉 Successfully generated my **first TTS audio** with Murf AI

---

### 🗓️ Day 2 – TTS API Integration

- 🔁 Connected **Murf's TTS API** to FastAPI backend
- 🧪 Built a basic UI with text input and audio playback
- 🎧 Achieved full **text-to-speech cycle** in browser
- 🛠️ Handled errors gracefully on both front and back end
- 📢 Shared my progress on LinkedIn with `#30DayVoiceAgent`

---

### 🗓️ Day 3 – Voice Agent UX

- 🖌️ Polished the UI with improved design (HTML/CSS)
- 🔄 Refactored API flow for smoother UX
- 💡 Learned how to make the voice interaction feel more natural
- 🙌 Thanked **Murf AI** publicly for enabling student creativity

---

### 🗓️ Day 4 – Echo Bot 🎤

- 🪞 Added a brand-new feature: **Echo Bot** section in the UI
- 🧩 Used the browser’s **MediaRecorder API** to:

  - Start and stop mic recordings
  - Instantly play back recorded audio

- 🧠 Learned how to work with real-time audio in the browser
- ✨ This will serve as the foundation for future **speech input** integration

---

### 🗓️ Day 5 – Audio Upload + Server Integration ☁️

- ⏺️ Extended the Echo Bot to **upload audio to my Python server**
- 🛠️ Built a new `/upload` API in **FastAPI** to:

  - Accept audio blob from frontend
  - Save it in an `/uploads` folder
  - Return file **name**, **type**, and **size**

- 🔔 Added a real-time **status message on UI** after upload
- 🔃 Improved end-to-end interactivity from mic → server → playback

---

### 🗓️ Day 6 – Transcription Integration ✍️

- 🧵 Created `/transcribe/file` endpoint on backend
- 📤 Accepts audio, returns **transcription** via **AssemblyAI**
- 🖥️ Integrated transcription into frontend UI
- 📜 Now have **record voice → upload → transcribe → display text** flow

---

### 🗓️ Day 7 – Voice-to-Voice with `/tts/echo` 🎤🔄🎙️

- 🆕 Backend endpoint: `/tts/echo`
- 🎙️ Flow:

  1. Accept audio → transcribe (AssemblyAI)
  2. Send text to Murf AI → generate new voice
  3. Return voice file URL to client

- 🔄 Full voice-to-voice pipeline now works: **User speaks → Server transcribes → Murf re-voices → Client plays**

---

### 🗓️ Day 8 – Building LLM Query Endpoint 🧠💬

- 🆕 Added a brand-new backend endpoint: **`/llm/query`** in FastAPI
- 📩 This endpoint:

  - Accepts a **JSON payload** containing `text` from the frontend
  - Sends the text to **Google Gemini API**
  - Returns the AI-generated response in **JSON format**

- ⚡ Used the `gemini-1.5-flash` model for quick replies
- 🛠️ Created a helper function `getResponseFromGemini()` to keep code clean
- 🚫 Implemented error handling for API issues and model mismatches
- 💡 This is the first step towards a **conversational AI** that can handle natural queries

---

### 🗓️ Day 9 – Audio-to-Audio AI Conversation 🎤🤖🎙️

- 🔄 Upgraded the `/llm/query` endpoint to **accept audio recordings** directly from the browser
- 📋 New flow:

  1. User records voice in browser
  2. Audio is sent to backend as `multipart/form-data`
  3. **AssemblyAI** transcribes the speech into text
  4. Transcription is sent to **Google Gemini API** for a reply
  5. AI reply is sent to **Murf AI** for lifelike TTS output
  6. Backend returns the generated audio to the frontend

- 🎧 On the frontend, the new voice plays instantly after generation
- ✨ Now the AI can **listen and talk back** without needing any text input

---

### 🗓️ Day 10 – Session-Based Chat Memory 🗂️🗣️

- 🧠 Added **context awareness** so the AI remembers what was said earlier in the conversation
- 🆕 New backend endpoint: **`/agent/chat/{session_id}`**
- 📋 Flow:

  1. Accepts **audio file** from client
  2. Transcribes it with **AssemblyAI**
  3. Saves message into **session chat history** keyed by `session_id`
  4. Sends **full conversation history** to Gemini for context-rich replies
  5. Adds AI reply to session memory
  6. Converts reply to speech with Murf AI and sends it back

- 🎯 Result: **Smooth, natural, and context-aware conversations** with the AI agent

---

### 🗓️ Day 11 – Robust Error Handling 🛡️⚙️

- 🔒 Added **try/except** blocks in FastAPI to catch backend errors
- 🛠️ Added **try/catch** in JavaScript to show clear error messages to users
- 📢 User now gets **friendly alerts** instead of cryptic error codes
- 📉 Reduced app crashes during network/API failures
- ✅ A more **reliable and user-friendly** experience overall

---

### 🗓️ Day 12 – Conversational Agent UI Revamp 🎨🖥️

- 🎯 Focused on **polishing the user interface** for better UX
- ✨ Key improvements:

  - **One-tap recording**: Start/stop with a single button
  - **Animated mic button**: Visual feedback while recording
  - **Auto-play replies**: No extra clicks to hear AI’s voice
  - **Mobile responsive design** for on-the-go testing
  - Removed unused sections to keep UI clean and minimal

- 📸 Updated UI screenshot:
  ![alt text](image.png)
- 🚀 Now the voice agent **feels like a real app**, not just a prototype

---

### 🗓️ Day 13 – Readme 🎨🖥️

-- Updated Readme.md

---

### 🗓️ Day 14 – Folder Structure 🎨🖥️

- Structured Folder setup
- created helper functions

---

### 🗓️ Day 15 – Websockets 🎨🖥️

- Today i created a endpoint /ws
- checked it on postman
- and it's working

---

### 🗓️ Day 15 – Websockets 🎨🖥️

Here’s a polished **LinkedIn post** draft for **Day 16 of your Voice Agent challenge** 👇

---

# 🎙️ Day 16

🔹 **What I built**
I implemented a system where the **client records audio and streams it live to the server** using **WebSockets**. Instead of collecting all chunks locally, the browser sends small packets of audio data to the server at regular intervals.

On the **server side**, these binary audio chunks are received and saved directly into a file — no transcription, LLM, or TTS yet, just **pure audio capture and streaming**.

🔹 **Why it matters**

- Enables **real-time audio handling**
- Scales better for longer recordings (no huge memory usage on client)
- Lays the foundation for real-time features like **live transcription, voice commands, or streaming TTS** in future iterations

---

# 🎙️ Day 17 – Streaming Transcription with AssemblyAI

## 🔹 Overview

Yesterday (Day 16), I implemented **real-time audio streaming** from the client to the server using **WebSockets**.  
Today, I extended that system by integrating **AssemblyAI’s Python SDK** to **transcribe the incoming audio stream**.

Instead of only saving raw audio, the server now connects to AssemblyAI’s **Streaming API**, transcribes the audio in real time, and prints the transcription to the console (or directly on the UI).

---

## 🔹 What I Built

1. **Client Side**

   - Captures microphone input
   - Streams audio chunks to the server via WebSockets at regular intervals

2. **Server Side**
   - Receives binary audio chunks from the client
   - Uses **AssemblyAI’s Python SDK** to stream audio to their API
   - Prints real-time transcription to the console (can also push to the UI)

---

## 🔹 Why It Matters

- Converts speech → text in **real time**
- Makes the system **interactive and dynamic**
- Lays the foundation for **voice commands, dialogue systems, and searchable transcripts**

---

## 🔹 Next Steps (Day 18 Preview)

AssemblyAI’s Streaming API also supports **turn detection**:

- Detects when a user **stops speaking**
- Sends a **WebSocket event to the client** signaling the end of a turn
- Displays the **final transcription** on the UI at the end of each turn

This will make the voice agent feel more **natural and conversational**.

---

## ⚙️ What You’ll Need

- **FastAPI** (Python)
- **Murf AI API key**
- **AssemblyAI API key**
- **Google Gemini API key**
- HTML, CSS, JS frontend
- `.env` file to store keys

---

## 💡 Tools I'm Using

| Tool             | Purpose                             |
| ---------------- | ----------------------------------- |
| Murf AI          | Text-to-Speech (TTS)                |
| FastAPI          | Backend API server                  |
| HTML/CSS/JS      | UI for interaction and playback     |
| MediaRecorder    | Echo Bot mic capture + playback     |
| FormData         | Uploading audio blob to the backend |
| AssemblyAI / STT | Transcribing recorded audio         |
| Gemini API       | AI-generated conversation           |

---

# 🛠 Installation & Run Instructions

### 📂 Project Structure

```
├── 📁 .git/ 🚫 (auto-hidden)
├── 📁 .venv/ 🚫 (auto-hidden)
├── 📁 Agent/
│   ├── 📁 Routes/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   └── 🐍 agent_chat.py
│   ├── 📁 Services/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   ├── 🐍 Gemini_service.py
│   │   ├── 🐍 Stt_service.py
│   │   └── 🐍 Tts_service.py
│   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   ├── 📁 utils/
│   │   ├── 📁 __pycache__/ 🚫 (auto-hidden)
│   │   └── 🐍 logging.py
│   ├── 🌐 index.html
│   ├── 🐍 main.py
│   ├── 📄 script.js
│   ├── 🎨 style.css
│   └── 📄 tempCodeRunnerFile.js
├── 🔒 .env 🚫 (auto-hidden)
├── 🚫 .gitignore
├── 📖 README.md
├── 📄 Requirement.txt
└── 🖼️ image.png

```

---

### 🔑 API Keys

Create `.env` file in root:

```env
MURF_API_KEY=your_murf_api_key
ASSEMBLY_API_KEY=your_assemblyai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

### 📥 Installation Steps

1️⃣ **Clone the repo**

```bash
git clone https://github.com/Vishalpandey1799/Murf-AI-Voice-Agent.git
cd Murf-AI-Voice-Agent
```

2️⃣ **Create and activate virtual environment**

- **Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

- **Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3️⃣ **Install dependencies**

```bash
pip install -r requirement.txt
```

4️⃣ **Run the FastAPI server**

```bash
uvicorn main:app --reload
```

---

## 🙌 Special Thanks

Huge thanks to **Murf AI** for organizing this amazing challenge and encouraging builders to explore the world of voice-first interfaces.
Your tools are enabling the next generation of interactive agents 💜

---

## 🔗 Follow My Progress

📍 Catch my updates on LinkedIn with: [#30DayVoiceAgent](https://www.linkedin.com/in/vishal-kumar-3835a9330/)
Let’s build cool voice stuff together!

---
