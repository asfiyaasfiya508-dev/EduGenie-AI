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


def answer_question(question):
    """
    Answer a student's question using Gemini.
    """

    if not question or not question.strip():
        return "Please enter a question."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.
Use simple language that a student can understand.
Give an example when useful.

Student Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Error while getting the answer: {str(error)}"