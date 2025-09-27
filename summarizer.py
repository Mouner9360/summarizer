import google.generativeai as genai
import json

def summarize_text(transcript, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        "You are an assistant that summarizes meeting transcripts.\n"
        "Transcript:\n"
        f"{transcript}\n\n"
        "Output a JSON object with keys:\n"
        "summary: 3-4 sentence summary,\n"
        "action_items: list of action items,\n"
        "decisions: list of major decisions."
    )

    response = model.generate_content(prompt)
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback: return plain text if JSON parsing fails
        result = {"summary": response.text, "action_items": [], "decisions": []}
    return result
