from flask import Flask, request, send_file, render_template
import yt_dlp, os
from main import *

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <form action="/download" method="post">
        <input type="text" name="query" placeholder="Paste Spotify playlist ID:">
        <button type="submit">Download MP3</button>
    </form>
    """

@app.route("/download", methods=["POST"])
def download():
    id = request.form["query"]

    print(main(id))
if __name__ == "__main__":
    app.run(debug=True)
