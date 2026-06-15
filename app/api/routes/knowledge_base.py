from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["AI Knowledge Base"])


@router.post("/documents")
async def create_document(
    filename: str = Query(...), session: AsyncSession = Depends(get_db)
):
    repository = DocumentRepository(session)
    service = DocumentService(repository)
    return await service.create_document(filename)


@router.get("/documents")
async def get_all_documents(session: AsyncSession = Depends(get_db)):
    repository = DocumentRepository(session)
    service = DocumentService(repository)
    return await service.get_all_documents()
