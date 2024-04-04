import os
import google.generativeai as genai

GOOGLE_API_KEY= os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def ai_summarizer(original_text):
    # Generate a summary of the event description using the GEMINI model.
    response = model.generate_content(f"Summarize this: {original_text}")
    print(response.text)
    return response.text
