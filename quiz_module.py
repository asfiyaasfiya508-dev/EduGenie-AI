import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )

client = genai.Client(api_key=API_KEY)


def clean_json_block(text):
    """
    Remove Markdown code blocks if Gemini returns JSON
    inside ```json ... ``` .
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_quiz(topic):
    """
    Generate exactly 3 MCQs with 4 options each.
    """

    if not topic or not topic.strip():
        return {"error": "Please enter a topic for the quiz."}

    prompt = f"""
Create a quiz for a student based on the following topic:

{topic}

Generate exactly 3 multiple-choice questions.

Rules:
1. Generate exactly 3 questions.
2. Each question must have exactly 4 options.
3. Give one correct answer.
4. Give a short explanation for the correct answer.
5. Return ONLY valid JSON.
6. Do not add Markdown or extra text.

Use this JSON format:

{{
    "questions": [
        {{
            "question": "Question here",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "explanation": "Explanation here"
        }}
    ]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        cleaned_response = clean_json_block(response.text)

        quiz = json.loads(cleaned_response)

        return quiz

    except json.JSONDecodeError:
        return {
            "error": "The quiz response was not valid JSON.",
            "raw_response": response.text
        }

    except Exception as error:
        return {
            "error": f"Quiz generation error: {str(error)}"
        }