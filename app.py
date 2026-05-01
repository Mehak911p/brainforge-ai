from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_msg}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

    user_msg = request.json.get("message")

    # TEMP reply (no API yet)
    return jsonify({"reply": "You said: " + user_msg})

if __name__ == "__main__":
    app.run()
