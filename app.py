import os
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-change-me")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a friendly, helpful AI assistant. "
    "Keep replies concise, warm, and easy to understand."
)


@app.route("/")
def index():
    session.setdefault("history", [])
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
      history = session.get("history", [])
    history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        reply = completion.choices[0].message.content or ""
    except Exception as exc:
        app.logger.exception("OpenAI call failed")
        return jsonify({"error": f"AI request failed: {exc}"}), 500

    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-20:]

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    session["history"] = []
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
