from fastapi import APIRouter, Depends
from app.services.document_service import DocumentService
from app.schemas.schema import DocumentCreate, DocumentRead
from app.api.dependencies.document import get_document_service

router = APIRouter(prefix="/documents", tags=["AI Knowledge Base"])


@router.post("/", response_model=DocumentRead)
async def create_document(
    data: DocumentCreate, service: DocumentService = Depends(get_document_service)
):
    return await service.create_document(data.filename)


@router.get("/", response_model=list[DocumentRead])
async def get_all_documents(service: DocumentService = Depends(get_document_service)):
    return await service.get_all_documents()
