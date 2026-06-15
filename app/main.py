from fastapi import FastAPI
from app.core.db import engine

from app.api.routes.knowledge_base import router as documents_router

from contextlib import asynccontextmanager
from app.core.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI KNOWLEDGE-BASE API", lifespan=lifespan)


app.include_router(documents_router)
