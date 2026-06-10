import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(query: str,context: str,history: str) -> str:

    prompt = f"""
You are a helpful assistant.

Chat History:
{history}

Context:
{context}

Question:
{query}

Answer using the provided context whenever possible.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text



import json


def extract_booking_info(message: str):

    prompt = f"""
Extract interview booking information.

Return ONLY valid JSON.

{{
    "is_booking": true,
    "name": "",
    "email": "",
    "date": "",
    "time": ""
}}

Message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return json.loads(response.text)