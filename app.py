import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from transcribe import normalize_audio, transcribe_audio
from summarizer import summarize_text

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create the Flask app
app = Flask(__name__)

# A simple health check route
@app.route("/")
def home():
    return "Backend is running!"

# Main route to handle uploads
@app.route("/api/transcribe", methods=["POST"])
def handle_transcription():
    """
    Expects a form-data POST with:
      - file: the audio file to process
    Returns:
      JSON with transcript + summary + action_items
    """
    # 1️⃣ Check that a file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files['file']

    # 2️⃣ Save the raw file temporarily
    raw_path = os.path.join("tmp_uploads", uploaded_file.filename)
    os.makedirs("tmp_uploads", exist_ok=True)
    uploaded_file.save(raw_path)

    # 3️⃣ Normalize audio for transcription
    normalized_path = raw_path.replace(".", "_normalized.")
    normalize_audio(raw_path, normalized_path)

    # 4️⃣ Send to Gemini for transcription
    transcript = transcribe_audio(normalized_path, GEMINI_API_KEY)

    # 5️⃣ Summarize transcript using Gemini
    summary_result = summarize_text(transcript, GEMINI_API_KEY)

    # 6️⃣ Return JSON response to frontend
    return jsonify({
        "transcript": transcript,
        **summary_result  # merges keys: summary, action_items, etc.
    })

if __name__ == "__main__":
    # Run the Flask dev server
    # debug=True auto-restarts on code changes
    app.run(host="0.0.0.0", port=5000, debug=True)
