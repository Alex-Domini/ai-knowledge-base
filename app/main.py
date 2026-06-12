from fastapi import FastAPI, Depends
from app.repositories.document_repository import DocumentRepository
from app.core.db import get_db, engine

from contextlib import asynccontextmanager
from app.core.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI KNOWLEDGE-BASE API", lifespan=lifespan)


@app.get("/")
def home_page():
    return {"message": "Привет!"}


@app.get("/db-check")
async def get_document(session=Depends(get_db)):
    repository = DocumentRepository(session)
    result = await repository.check_connection()

    return result
