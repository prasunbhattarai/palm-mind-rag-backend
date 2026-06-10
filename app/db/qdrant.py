from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    host="qdrant",
    port=6333
)

COLLECTION_NAME = "documents"


def create_collection(vector_size: int):

    collections = client.get_collections().collections

    if COLLECTION_NAME not in [c.name for c in collections]:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )