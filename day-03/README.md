🎯 **Day 03 – Text-to-Speech with Murf AI**

Welcome to Day 3 of the **30 Days of Voice Agents Challenge**!  
Today’s focus was on adding **dynamic voice selection** by fetching voice options from Murf AI and letting users choose before generating speech.

🧠 **What We Built**

A voice app that:
- Accepts text input from the user  
- Dynamically fetches available voice options from the Murf API  
- Lets the user select a voice before generating speech  
- Sends both the text and selected voice to the Murf API  
- Plays the resulting audio in the browser

🛠 **Tech Stack**

- **Backend**: `FastAPI`, `python-dotenv`, `requests`  
- **Frontend**: `HTML`, `Bootstrap`, `JavaScript`  
- **Voice API**: Murf AI – `/voices` and `/speech/generate` endpoints


🔐 **Environment Variables**

Create a `.env` file in the root of `day-03/`: <br>
MURF_API_KEY=your_actual_murf_api_key

Make sure to use a valid voice ID in the request payload (e.g., `en-US-natalie`).

▶️ **Run the App**

cd day-03/ <br>
pip install -r requirements.txt <br>
uvicorn main:app --reload

Visit http://localhost:8000 in your browser.

🧪 **Test Input**

Try typing something like: <br>
"This is Day 2 of the Voice Agent Challenge."

Select a voice from the dropdown, then click Generate Voice.

If fetching voices from the API fails, a fallback list of voices is used automatically.
