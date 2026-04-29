from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Your app is working 🚀"

@app.route("/api/test")
def test():
    return jsonify({"message": "API working successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
