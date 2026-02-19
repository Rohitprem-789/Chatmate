from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

messages = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    messages.append({
        "type": "text",
        "user": data["user"],
        "message": data["message"]
    })
    return jsonify({"status": "ok"})

@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    audio = request.files["audio"]
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".webm"
    path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(path)

    messages.append({
        "type": "audio",
        "file": filename
    })

    return jsonify({"status": "ok"})

@app.route("/messages")
def get_messages():
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
