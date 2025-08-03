🎯 **Day 02 – Text-to-Speech with Murf AI**

Welcome to Day 2 of the **30 Days of Voice Agents Challenge**!  
Today’s focus is on turning user input into speech using the **Murf AI Text-to-Speech (TTS) API** and playing it back in the browser — powered by **FastAPI**, **Bootstrap**, and plain JavaScript.

🧠 **What We Built**

A voice app that:
- Accepts text input from the user
- Sends it to the Murf API for TTS generation
- Plays back the generated audio directly in the browser

🛠 **Tech Stack**

- **Backend**: `FastAPI`, `python-dotenv`, `requests`  
- **Frontend**: `HTML`, `Bootstrap`, `JavaScript`  
- **Voice API**: Murf AI – `/speech/generate` endpoint

🔐 **Environment Variables**

Create a `.env` file in the root of `day-02/`: <br>
MURF_API_KEY=your_actual_murf_api_key

Make sure to use a valid voice ID in the request payload (e.g., `en-US-natalie`).

▶️ **Run the App**

cd day-02/ <br>
pip install -r requirements.txt <br>
uvicorn main:app --reload

Visit http://localhost:8000 in your browser.

🧪 **Test Input**

Try typing something like: <br>
"This is Day 2 of the Voice Agent Challenge."

Click Generate Voice and listen!
