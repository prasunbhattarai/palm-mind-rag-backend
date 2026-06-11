from fastapi import APIRouter, UploadFile, File, Query
from app.services.ingestion import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest_file(
    file: UploadFile = File(...),
    strategy: str = Query("recursive", pattern="^(fixed|recursive)$")
):
    result = ingest_document(file.file, file.filename, strategy)
    return result