# Day 26: Improving the Agent's Special Skill with Intelligence

Welcome to Day 26 of the 30 Days of Voice Agents Challenge\! Today, we've made a significant improvement to our agent's web search skill by giving it the intelligence to decide *when* a search is necessary.

## 🧠 What We Built

  * **Intelligent Skill Selection**: Instead of relying on specific keywords, the agent now uses a lightweight LLM prompt to analyze the user's query and determine if a web search is required to provide an accurate answer.
  * **Automatic Tool Use**: MARVIS can now automatically trigger its web search skill based on the context of the conversation, making the interaction more natural and seamless.
  * **A Smarter, More Autonomous Agent**: This enhancement makes the agent more autonomous and efficient. It now knows when to rely on its internal knowledge and when to seek out real-time information from the web, improving both the speed and relevance of its responses.

-----

## 🛠 Tech Stack

The tech stack remains the same, but the underlying logic for how the agent decides to use its tools has been upgraded.

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
5.  **Open your browser** and visit `http://localhost:8000`. Grant microphone permissions and try asking a question that requires current information.

-----

## 📂 Project Structure

The project structure has been updated to include the new intelligent decision-making logic in the `llm.py` service.

```
AI Voice Agent/
├── main.py      # Updated to call the new web search check
├── config.py
├── services/
│   ├── llm.py   # Updated with the should_search_web function
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

  * **Day 01 - 24**: Foundational work from setting up the server to giving the agent a persona.
  * **Day 25**: Equipped the agent with a web search skill using a tool-use paradigm.
  * **Day 26**: Made the web search skill intelligent by adding automatic detection for when it's needed.
