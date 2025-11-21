# app.py
from flask import Flask, render_template, request, jsonify
import os
import re
import string
import requests

app = Flask(__name__)

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return " ".join(text.split())

# Free public Gemini proxy (no key needed!)
GEMINI_PROXY = "https://generative-api-gemini-proxy.vercel.app/api/gemini"

def ask_gemini_free(question):
    payload = {
        "contents": [{"role": "user", "parts": [{"text": question}]}]
    }
    try:
        response = requests.post(GEMINI_PROXY, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Gemini is busy right now. Try again in a few seconds."
    except:
        return "Network error. Check your internet."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    
    if not question:
        return jsonify({"answer": "Please type a question."})
    
    processed = preprocess(question)
    
    # Only one model now — super fast & free
    answer = ask_gemini_free(processed)
    
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)