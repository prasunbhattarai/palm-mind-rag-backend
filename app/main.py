from fastapi import FastAPI
from app.api.booking import router as booking_router
from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router

app = FastAPI()



