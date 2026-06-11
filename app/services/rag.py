from app.db.qdrant import get_client, COLLECTION_NAME
from app.utils.embeddings import get_embedding


def search_documents(query: str, top_k: int = 3):
    embedding = get_embedding(query)
    try:
        results = get_client().query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            limit=top_k,
        )
    except Exception:
        return []
    return [hit.payload["text"] for hit in results.points] if results.points else []
