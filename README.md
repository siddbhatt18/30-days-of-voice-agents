🎙️ **30 Days of Voice Agents Challenge**

Welcome to my repository for the **30 Days of Voice Agents** challenge, organized by [Murf AI](https://murf.ai). This challenge is all about building voice-powered apps, experimenting with AI APIs, and leveling up with tools like FastAPI, Flask, and JavaScript — over the course of 30 days.

🚀 **What is this Challenge?**

The goal is to create 30 mini voice agent projects in 30 days. Each day focuses on a new concept — from UI interactions to speech synthesis and voice APIs.

Whether it's a simple button with audio feedback or an advanced AI agent, every day's project builds upon the last.

📁 **Repository Structure**

Each day's code lives in its own folder:

30-days-of-voice-agents/
├── day-01/ # FastAPI + Bootstrap Welcome Page
├── day-02/ # TTS API Integration (Text to Speech)
├── ...
├── README.md # You're here
├── .gitignore

Inside each day's folder:
- `main.py` or `app.py` – Backend logic (FastAPI or Flask)
- `templates/` – Jinja2 HTML files
- `static/` – JS or CSS assets
- `requirements.txt` – Dependencies
- `README.md` – Specifics for that day’s project

🛠 **Technologies Used**

- **Python**
  - FastAPI ⚡ / Flask
  - `requests`, `python-dotenv`, etc.
- **Frontend**
  - HTML / CSS / Bootstrap
  - JavaScript
- **Voice Tools**
  - Murf AI TTS APIs (Text-to-Speech)
  - Audio playback in browser
- **Deployment (Optional)**
  - Uvicorn / Replit / Render

▶️ **Running a Project**

To run a day's project locally:

cd day-01  # or day-02, etc.
pip install -r requirements.txt
uvicorn main:app --reload  # or python app.py if using Flask

Then open your browser at:
http://localhost:8000
