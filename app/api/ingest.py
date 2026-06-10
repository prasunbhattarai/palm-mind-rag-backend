from fastapi import APIRouter, UploadFile, File, Query
from app.services.ingestion import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest_file(
    file: UploadFile = File(...),
    strategy: str = Query("recursive", regex="^(fixed|recursive)$")
):
    result = ingest_document(file.file, strategy)
    return result