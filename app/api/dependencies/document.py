from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.core.db import get_db


async def get_document_service(
    session: AsyncSession = Depends(get_db),
) -> DocumentService:
    repository = DocumentRepository(session)
    service = DocumentService(repository)
    return service
