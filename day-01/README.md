# Day 01: Basic FastAPI Server with Bootstrap UI

Welcome to Day 1 of the 30 Days of Voice Agents Challenge\! Today’s focus is on initializing a Python backend using **FastAPI**, creating a basic `index.html` file, and serving it from the server.

## 🧠 What We Built

A simple web application that:

  - Serves a static HTML page using a FastAPI backend.
  - Includes a basic user interface styled with Bootstrap.
  - Features a button that triggers a JavaScript alert.

## 🛠 Tech Stack

  - **Backend**: `FastAPI`, `uvicorn`, `Jinja2`
  - **Frontend**: `HTML`, `Bootstrap`, `JavaScript`

## 🚀 Run the App

1.  **Navigate to the project directory:**
    ```bash
    cd day-01/
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
4.  **Open your browser** and visit [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000).

## 📂 Project Structure

```
day-01/
├── main.py # Backend logic (FastAPI)
├── templates/
│   └── index.html # Jinja2 HTML file
├── static/
│   └── script.js # JavaScript assets
└── requirements.txt # Dependencies
```

## ✅ Completed Days

  - **Day 01**: Set up a basic FastAPI server with a Bootstrap UI.
