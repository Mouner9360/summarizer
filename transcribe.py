from pydub import AudioSegment
import google.generativeai as genai

def normalize_audio(input_path, output_path):
    """Convert to mono 16kHz WAV for better transcription."""
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")

def transcribe_audio(file_path, api_key):
    """Send audio to Gemini for transcription."""
    genai.configure(api_key=api_key)

    # Gemini has a built-in audio transcribe model (gemini-2.5-flash handles audio)
    model = genai.GenerativeModel("gemini-2.5-flash")
    with open(file_path, "rb") as f:
        response = model.generate_content([{"mime_type": "audio/wav", "data": f.read()}])
    # The text output from Gemini
    return response.text.strip()