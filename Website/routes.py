import json
import shutil, json
from flask import Flask, after_this_request, render_template, request, jsonify, Response, send_file
import sys
import os
import threading
import queue
from Backend.spotipyMain import sp

# Add the functionality folder to the import path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Backend'))

from Backend.main import main as download_playlist
from Backend.spotipyMain import verify

progress_queue = queue.Queue()
download_tasks = {}

def register_routes(app: Flask):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/download', methods=['POST'])
    def download():
        playlist_url = request.form.get('playlist_url')
        playlist_id = "abc"
        try:
            playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        except (IndexError, AttributeError) as e:
            return jsonify({"status": "error", "message": "Invalid playlist URL format"}), 400
        
        if not verify(playlist_id):
            return jsonify({"status": "error", "message": "Invalid Spotify playlist URL"}), 400

        stop_flag = {'should_stop': False}

        def run_download():
            def progress_callback(song, current, total):
                if stop_flag['should_stop']:
                    progress_queue.put({"cancelled": True})
                    return False  # Signal to stop
                
                progress = int((current / total) * 100)
                msg = {"song": song if song else "", "current": current, "total": total, "progress": progress}
                print(msg, flush=True)
                progress_queue.put(json.dumps(msg))
                return True  # Continue downloading
            download_playlist(playlist_url, progress_callback)
            progress_queue.put(json.dumps({
                "done": True, 
                "zip_ready": True,
                "zip_id": playlist_id  # or whatever identifier you're using
            }))
            if playlist_id in download_tasks:
                del download_tasks[playlist_id]
            
            
        
        thread=threading.Thread(target=run_download, daemon=True)
        download_tasks[playlist_id] = {'thread': thread, 'stop_flag': stop_flag}
        thread.start()

        return jsonify({"status": "success", "message": f"Started downloading playlist {sp.user_playlist(user=None, playlist_id=playlist_id, fields='name')['name']}"})

    @app.route('/get_zip/<zip_id>', methods=['GET'])
    def get_zip(zip_id):
        zip_path = f'Songs/{zip_id}.zip'
        if not os.path.exists(zip_path):
            return jsonify({"status": "error", "message": f"Zip file not found at {zip_path}"}), 404
    

        @after_this_request
        def cleanup(response):
            try:
                # Add a small delay to ensure file is released
                import threading
                def delayed_delete():
                    import time
                    time.sleep(2)  # Wait 2 seconds for file handle to close
                    try:
                        os.remove(zip_path)
                    except Exception as e:
                        print(f"Error cleaning up: {e}", flush=True)
                
                thread = threading.Thread(target=delayed_delete)
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"Error setting up cleanup: {e}", flush=True)
            return response
        
        return send_file(
            "../"+zip_path,
            as_attachment=True,
            download_name=f'{zip_id}.zip',
            mimetype='application/zip'
        )

    @app.route('/progress')
    def progress_stream():
        def stream():
            while True:
                msg = progress_queue.get()
                yield f"data: {msg}\n\n"
                print("Sent progress message:", msg, flush=True)
                if "done\": true" in msg or "cancelled" in msg:
                    break
        return Response(stream(), mimetype="text/event-stream")


# if __name__ == '__main__':
#     app.run(debug=True)
