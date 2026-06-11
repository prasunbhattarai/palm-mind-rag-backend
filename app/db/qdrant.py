import os
from functools import cache

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "documents"


@cache
def get_client():
    return QdrantClient(
        host=os.getenv("QDRANT_HOST", "qdrant"),
        port=6333
    )


def create_collection(vector_size: int):
    client = get_client()
    collections = client.get_collections().collections

    if COLLECTION_NAME not in [c.name for c in collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )