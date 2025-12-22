from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json(force=True)

    url = data.get("url")
    fmt = data.get("format", "mp4").lower()  # mp4 | mp3

    if not url:
        return jsonify({"error": "url boşdur"}), 400

    file_id = str(uuid.uuid4())

    # ===== MP3 =====
    if fmt == "mp3":
        output_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp3")
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", output_path,
            url
        ]

    # ===== MP4 =====
    else:
        output_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")
        cmd = [
            "yt-dlp",
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", output_path,
            url
        ]

    try:
        subprocess.run(cmd, check=True)
        return jsonify({
            "status": "ok",
            "format": fmt,
            "file": f"/file/{os.path.basename(output_path)}"
        })
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "yt-dlp xətası", "detail": str(e)}), 500


@app.route("/file/<filename>", methods=["GET"])
def get_file(filename):
    path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "file tapılmadı"}), 404

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
