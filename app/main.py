from fastapi import FastAPI
from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router
from app.db.models import Base
from app.db.postgres import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(chat_router)
app.include_router(ingest_router)
app.include_router(booking_router)



