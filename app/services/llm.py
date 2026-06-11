import json
import os
import re
from functools import cache

from google import genai


@cache
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(query: str, context: str, history: str):
    client = get_client()

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


def extract_booking_info(message: str):
    client = get_client()

    prompt = f"""
Extract interview booking information. Return date in YYYY-MM-DD format and time in HH:MM 24-hour format.

Return ONLY valid JSON.

{{"is_booking": true, "name": "", "email": "", "date": "", "time": ""}}

Message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()

    return json.loads(text)