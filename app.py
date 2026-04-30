from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>BrainForge AI</h2>
    <input id='msg' placeholder='Ask something'>
    <button onclick='send()'>Send</button>
    <p id='res'></p>

    <script>
    async function send(){
        let msg = document.getElementById('msg').value;
        let res = await fetch('/chat', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({message: msg})
        });
        let data = await res.json();
        document.getElementById('res').innerText = data.reply;
    }
    </script>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    # TEMP reply (no API yet)
    return jsonify({"reply": "You said: " + user_msg})

if __name__ == "__main__":
    app.run()
