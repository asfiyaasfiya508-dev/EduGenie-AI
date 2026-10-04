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


def get_learning_recommendations(topic, level="beginner"):
    """
    Generate a personalized learning path using Gemini.
    """

    if not topic or not topic.strip():
        return "Please enter a topic for the learning path."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Create a structured learning path for the following topic:

Topic: {topic}

Learner level: {level}

The learning path should include:

1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Suggested timeline
5. Practice activities
6. Useful learning resources such as videos,
   articles, books, or documentation

Make the plan simple, clear, and suitable for a student.

Adapt the recommendations to the learner's level.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"Learning path generation error: {str(error)}"