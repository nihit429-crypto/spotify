from flask import Flask, jsonify, send_from_directory, render_template, request
import os

app = Flask(__name__)
SONG_FOLDER = "songs"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/songs")
def list_songs():
    songs = []
    # Just list the files exactly as they are. 
    # Since you will rename them, the filename IS the title.
    for filename in os.listdir(SONG_FOLDER):
        if filename.lower().endswith((".mp3", ".mp4", ".m4a", ".wav")):
            
            # Title is just the filename without extension
            title = os.path.splitext(filename)[0]
            
            songs.append({
                "title": title, 
                "file": filename,
                "url": f"/songs/{filename}"
            })
            
    songs.sort(key=lambda x: x["title"].lower())
    return jsonify(songs)

@app.route("/rename", methods=["POST"])
def rename_song():
    data = request.json
    old_filename = data.get("old_filename")
    new_name = data.get("new_name")

    if not old_filename or not new_name:
        return jsonify({"success": False, "error": "Missing data"})

    # Get the file extension (e.g., .mp4)
    ext = os.path.splitext(old_filename)[1]

    # Create the new filename (Name + Extension)
    new_filename = new_name.strip() + ext

    old_path = os.path.join(SONG_FOLDER, old_filename)
    new_path = os.path.join(SONG_FOLDER, new_filename)

    try:
        os.rename(old_path, new_path)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/songs/<path:filename>")
def stream_song(filename):
    return send_from_directory(SONG_FOLDER, filename)

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(SONG_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs(SONG_FOLDER, exist_ok=True)
    app.run(debug=True)