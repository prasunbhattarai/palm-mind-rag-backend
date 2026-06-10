import uuid

from qdrant_client.models import PointStruct

from app.db.qdrant import (
    client,
    create_collection,
    COLLECTION_NAME
)

from app.utils.pdfreader import read_all_pages
from app.utils.chunking import (
    fix_chunking,
    recursive_chunk
)
from app.utils.embeddings import get_embedding


def ingest_document(
    file_path: str,
    strategy: str
):

    text = read_all_pages(file_path)

    if strategy == "fixed":
        chunks = fix_chunking(text)

    elif strategy == "recursive":
        chunks = recursive_chunk(text)

    else:
        raise ValueError(
            "Invalid chunking strategy"
        )

    if not chunks:
        return {
            "status": "error",
            "message": "No text extracted"
        }

    first_embedding = get_embedding(
        chunks[0]
    )

    create_collection(
        len(first_embedding)
    )

    points = []

    for i, chunk in enumerate(chunks):

        if i == 0:
            embedding = first_embedding
        else:
            embedding = get_embedding(
                chunk
            )

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "chunk_index": i,
                    "source": file_path
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return {
        "status": "success",
        "chunks": len(chunks)
    }