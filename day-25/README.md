# Day 25: Equipping the Agent with a Special Skill - Web Search

Welcome to Day 25 of the 30 Days of Voice Agents Challenge\! Today, we've given our agent a significant upgrade by equipping it with a special skill: the ability to search the web for real-time information.

## 🧠 What We Built

  * **Tool-Using Agent**: We have implemented a "function calling" or "tool use" paradigm. The agent's underlying LLM can now intelligently decide when a user's query cannot be answered from its training data and requires external information.
  * **Live Web Search Capability**: A web search tool, powered by SerpAPI, has been integrated into our agent. When triggered, it performs a live Google search to gather the latest information on a given topic.
  * **Dynamic, Two-Step Responses**: For queries requiring current information, the agent now follows a two-step process:
    1.  It first uses the web search tool to find relevant, up-to-date context.
    2.  It then uses this new context to formulate a comprehensive and accurate answer for the user.
  * **A More Knowledgeable Agent**: By breaking the boundaries of its static training data, our agent is now more powerful, capable of discussing current events and providing information that is much more recent and relevant.

-----

## 🛠 Tech Stack

The core tech stack remains the same, with the addition of a new library for the web search functionality.

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
3.  **Create a `.env` file** and add your API keys:
    ```
    MURF_API_KEY="your_murf_api_key_here"
    ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    GEMINI_API_KEY="your_gemini_api_key_here"
    SERPAPI_API_KEY="your_serpapi_api_key_here"
    ```
4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
5.  **Open your browser** and visit `http://localhost:8000`. Grant microphone permissions and ask it something about a recent event\!

-----

## 📂 Project Structure

The project structure is updated to include the new tool logic, which is managed within our LLM service.

```
AI Voice Agent/
├── main.py
├── config.py
├── services/
│   ├── llm.py      # Updated with function calling logic
│   ├── stt.py
│   └── tts.py
├── schemas.py
├── templates/
│   └── index.html
├── static/
│   ├── script.js
│   └── style.css
├── requirements.txt
└── .env
```

-----

## ✅ Completed Days

  * **Day 01 - 23**: Foundational work from setting up the server to full end-to-end integration.
  * **Day 24**: Gave the agent a distinct persona to make it more engaging.
  * **Day 25**: Equipped the agent with a web search skill using a tool-use paradigm.
