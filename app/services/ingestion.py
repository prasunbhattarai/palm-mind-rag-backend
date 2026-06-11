import uuid

from qdrant_client.models import PointStruct

from app.db.qdrant import get_client, create_collection, COLLECTION_NAME
from app.db.postgres import SessionLocal
from app.db.models import Document
from app.utils.pdfreader import read_all_pages, read_text_file
from app.utils.chunking import fixed_chunking, recursive_chunk
from app.utils.embeddings import get_embedding


def ingest_document(file, filename: str, strategy: str):

    if filename.endswith(".pdf"):
        text = read_all_pages(file)
    elif filename.endswith(".txt"):
        text = read_text_file(file)
    else:
        return {"status": "error", "message": "Unsupported file type"}

    if strategy == "fixed":
        chunks = fixed_chunking(text)

    elif strategy == "recursive":
        chunks = recursive_chunk(text)

    else:
        raise ValueError("Invalid chunking strategy")

    if not chunks:
        return {"status": "error", "message": "No text extracted"}

    first_embedding = get_embedding(chunks[0])

    create_collection(len(first_embedding))

    points = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            embedding = first_embedding
        else:
            embedding = get_embedding(chunk)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "chunk_index": i,
                    "source": filename
                }
            )
        )

    get_client().upsert(collection_name=COLLECTION_NAME, points=points)

    db = SessionLocal()
    doc = Document(filename=filename, chunk_strategy=strategy, chunks_count=len(chunks))
    db.add(doc)
    db.commit()
    db.close()

    return {
        "status": "success",
        "filename": filename,
        "chunks": len(chunks),
        "strategy": strategy
    }