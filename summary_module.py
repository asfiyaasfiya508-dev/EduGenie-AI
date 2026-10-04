import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )

client = genai.Client(api_key=API_KEY)


def summarize_text(text):
    """
    Summarize educational text using Gemini.
    """

    if not text or not text.strip():
        return "Please enter some text to summarize."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Summarize the following educational text in a concise
and easy-to-understand way.

Requirements:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple student-friendly language.
- Keep the meaning of the original text.
- Use bullet points when useful.

Text to summarize:

{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Summary generation error: {str(error)}"