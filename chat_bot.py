# chat_bot.py — dev-safe CORS + curriculum-aware lesson & chat
from flask import Flask, request, jsonify, make_response
import os, requests

app = Flask(__name__)

# ---- DEV CORS: allow everything (no cookies used) ----
@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        return make_response(("", 204))

# ---- Curriculum ----
CURRICULUM = {
    "u1": """Unit 1: What is AI?
Goals:
[Explain the goals in plaintext with no specaial formatting, seperate the different prompts by number]
1) Explain what artificial intelligence (AI) and machine learning (ML) are, basics of how they work; list AI use cases.
2) Describe ML types: supervised, unsupervised, reinforcement learning; and neural networks at a high level.
3) Explain large language models (LLMs), basics of how they work, and examples: ChatGPT, Gemini, DeepSeek.""",

    "u2": """Unit 2: Using Basic LLMs and Making API Calls
Goals:
[Explain the goals in plaintext with no specaial formatting, seperate the different prompts by number]
1) Explain basics of making AI API calls; practice building simple requests.
2) Mini project: send requests to a model from Python (e.g., POST JSON to an endpoint and print the reply)."""
}

# ---- Gemini config (set GEMINI_API_KEY in your environment) ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

def gemini_reply(user_text, system_text=None):
    if not GEMINI_API_KEY:
        return "Server is missing GEMINI_API_KEY."
    payload = {"contents": [{"parts": [{"text": user_text}]}]}
    if system_text:
        payload["system_instruction"] = {"parts": [{"text": system_text}]}
    r = requests.post(URL, json=payload, timeout=45)
    try:
        data = r.json()
    except Exception:
        return "AI error"
    if r.status_code != 200:
        return data.get("error", {}).get("message", "AI error")
    out = ""
    for c in data.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            out += p.get("text", "")
    return out.strip() or "…"

# ---------- Start lesson ----------
@app.route("/lesson/start", methods=["POST", "OPTIONS"])
def start_lesson():
    body = request.json or {}
    unit = (body.get("unit") or "u1").strip().lower()
    plan = CURRICULUM.get(unit, CURRICULUM["u1"])
    title = "Unit 1: What is AI?" if unit == "u1" else "Unit 2: Using Basic LLMs & API Calls"

    system = (
        "You are ProfAI, a clear, kind professor for total beginners.\n"
        f"Teach the following curriculum:\n{plan}\n\n"
        "Output format:\n"
        "• A short intro paragraph\n"
        "• 5 compact bullets covering the key ideas\n"
        "• One tiny, concrete example\n"
        "• End with a single check-for-understanding question\n"
        "Limit to ~200 words."
    )
    text = gemini_reply("Start the lesson now.", system_text=system)
    return jsonify({"title": title, "lesson": text})

# ---------- Chat (follow-ups) ----------
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    body = request.json or {}
    unit = (body.get("unit") or "u1").strip().lower()
    plan = CURRICULUM.get(unit, CURRICULUM["u1"])
    user_msg = str(body.get("message") or "").strip()
    if not user_msg:
        return jsonify({"reply": "Please type a question."}), 400

    system = (
        f"You are ProfAI teaching this curriculum:\n{plan}\n\n"
        "Answer in 3–6 short sentences, use simple language, prefer small examples. "
        "If asked about hands-on practice, suggest one tiny exercise. "
        "If Unit 1 topic 2b comes up, you may mention simulators.yobee.co.in as an example."
    )
    reply = gemini_reply(user_msg, system_text=system)
    return jsonify({"reply": reply})

# Health
@app.get("/healthz")
def health():
    return "ok", 200

if __name__ == "__main__":
    # Run on http://127.0.0.1:5000 (change PORT env if needed)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5055")))