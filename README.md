**🎙️ 30 Days of Voice Agents Challenge** 

Welcome to my repository for the 30 Days of Voice Agents challenge, organized by Murf AI. This challenge is all about building voice-powered apps, experimenting with AI APIs, and leveling up with tools like FastAPI and JavaScript over 30 days.

**What is this Challenge?** 

The goal is to create 30 mini voice agent projects in 30 days. Each day focuses on a new concept—from UI interactions to speech synthesis and voice APIs.

**Repository Structure**

- main.py – Backend logic (FastAPI)
- templates/ – Jinja2 HTML files
- static/ – JS or CSS assets
- requirements.txt – Dependencies
- README.md – Specifics for that day’s project

**Technologies Used**

- Python
- FastAPI
- requests, python-dotenv, uvicorn
- Frontend
- HTML / CSS / Bootstrap
- JavaScript (including the MediaRecorder API)
- AI & Voice Tools
- Murf AI API for Text-to-Speech (TTS)
- AssemblyAI API for Speech-to-Text (STT)

**Running a Project**

- cd day-##/
- pip install -r requirements.txt
- uvicorn main:app --reload
- http://127.0.0.1:8000.

**Completed Days**

- Day 01: Set up a basic FastAPI server with a Bootstrap UI. <br>
- Day 02: Simple Text-to-Speech (TTS) using the Murf AI API. <br>
- Day 03: Added client-side audio recording using the MediaRecorder API. <br>
- Day 04: Sent recorded audio from the frontend to the FastAPI backend. <br>
- Day 05: Transcribed uploaded audio using the AssemblyAI API. <br>
- Day 06: Integrated the TTS and STT features into a single, organized UI. <br>
- Day 07: Created an "Echo Bot" that transcribes user audio and speaks it back in a new voice. <br>

**Stay tuned for more!**
