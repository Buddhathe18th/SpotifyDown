from flask import Flask, render_template, request, jsonify, Response
import sys
import os
import threading
import queue

# Add the functionality folder to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Backend'))

from main import main as download_playlist
from spotipyMain import verify

progress_queue = queue.Queue()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    playlist_url = request.form.get('playlist_url')

    playlist_id = "abc"
    try:
        playlist_id=playlist_url.split("playlist/")[1].split("?")[0]
    except:
        pass
    
    if not verify(playlist_id):
        return jsonify({"status": "error", "message": "Invalid Spotify playlist URL"}), 400

    def run_download():
        def progress_callback(song, current, total):
            progress = int((current / total) * 100)
            msg = {"song": song, "current": current, "total": total, "progress": progress}
            progress_queue.put(msg)
        download_playlist(playlist_url, progress_callback)
        progress_queue.put({"done": True})
    
    threading.Thread(target=run_download, daemon=True).start()

    return jsonify({"status": "success", "message": f"Started downloading playlist {playlist_id}"})

@app.route('/progress')
def progress_stream():
    def stream():
        while True:
            msg = progress_queue.get()
            yield f"data: {msg}\n\n"
            if msg.get("done"):
                break
    return Response(stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True)
