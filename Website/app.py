from flask import Flask, render_template, request, jsonify
import sys
import os
import threading

# Add the functionality folder to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Backend'))

from main import main as download_playlist
from spotipyMain import verify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    playlist_url = request.form.get('playlist_url')

    playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
    
    if not verify(playlist_id):
        return jsonify({"status": "error", "message": "Invalid Spotify playlist URL"}), 400

    threading.Thread(target=download_playlist, args=(playlist_id,)).start()

    return jsonify({"status": "success", "message": f"Started downloading playlist {playlist_id}"})

if __name__ == '__main__':
    app.run(debug=True)
