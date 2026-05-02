from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_msg
        )
        reply = response.output_text

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})

if __name__ == "__main__":
    app.run()
