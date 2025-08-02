from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Day 1 of the 30 Days of Voice Agents Challenge!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
