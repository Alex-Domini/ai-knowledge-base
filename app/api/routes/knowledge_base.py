from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.schemas.schema import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["AI Knowledge Base"])


@router.post("/", response_model=DocumentCreate)
async def create_document(
    data: DocumentCreate, session: AsyncSession = Depends(get_db)
):
    repository = DocumentRepository(session)
    service = DocumentService(repository)
    return await service.create_document(data.filename.strip().lower())


@router.get("/", response_model=list[DocumentRead])
async def get_all_documents(session: AsyncSession = Depends(get_db)):
    repository = DocumentRepository(session)
    service = DocumentService(repository)
    return await service.get_all_documents()
