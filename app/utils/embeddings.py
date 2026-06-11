import os
from functools import cache

from google import genai


@cache
def get_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def get_embedding(text: str) -> list[float]:
    client = get_client()
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values