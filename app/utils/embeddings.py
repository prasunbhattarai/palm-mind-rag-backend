import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )

    return response.embeddings[0].values

