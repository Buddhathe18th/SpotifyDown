from flask import Flask, Response, render_template_string, request
import time
from main import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
    <form action="/start" method="post">
        <input type="text" name="query" placeholder="Spotify ID">
        <button type="submit">Start Download</button>
    </form>
    <div id="progress"></div>

    <script>
    const evtSource = new EventSource("/progress");
    evtSource.onmessage = function(event) {
        document.getElementById("progress").innerHTML += event.data + "<br>";
    };
    </script>
    """)

progress_messages = []

@app.route("/start", methods=["POST"])
def start():
    global progress_messages
    query = request.form["query"]


    import threading
    threading.Thread(target=test, args=(query,)).start()
    return "Started! Open console above to watch progress."

@app.route("/progress")
def progress():
    def event_stream():
        global progress_messages
        last_index = 0
        while True:
            if len(progress_messages) > last_index:
                msg = progress_messages[last_index]
                last_index += 1
                yield f"data: {msg}\n\n"
            time.sleep(1)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)