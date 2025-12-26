from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

os.makedirs("downloads", exist_ok=True)

@app.route("/")
def home():
    return "YT-DLP SERVER IS RUNNING"

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")

    filename = f"{uuid.uuid4()}.mp4"
    path = f"downloads/{filename}"

    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", path,
        url
    ])

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)