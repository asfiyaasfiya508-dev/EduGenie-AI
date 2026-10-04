import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=API_KEY)


def explain_topic(topic):
    if not topic or not topic.strip():
        return "Please enter a topic to explain."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Explain the following topic to a beginner student.

Requirements:
- Use very simple English.
- Explain clearly and briefly.
- Use headings or bullet points when useful.
- Give one simple example.
- Avoid complicated technical words unless necessary.

Topic:
{topic}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Explanation error: {str(error)}"