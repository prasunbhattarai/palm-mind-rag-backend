from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router
from app.api.booking import router as booking_router
from app.db.models import Base
from app.db.postgres import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(booking_router)
app.include_router(ingest_router)



