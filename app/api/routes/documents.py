from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.services.document_service import DocumentService
from app.schemas.schema import DocumentCreate, DocumentRead
from app.api.dependencies.document import get_document_service

router = APIRouter(prefix="/documents", tags=["AI Knowledge Base"])


@router.post("/", response_model=DocumentRead)
async def create_document(
    data: DocumentCreate, service: DocumentService = Depends(get_document_service)
):
    return await service.create_document(data.filename)


@router.post("/upload", response_model=DocumentRead)
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    filename = file.filename
    if filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )
    document = await service.create_document(filename)
    return document


@router.get("/", response_model=list[DocumentRead])
async def get_all_documents(service: DocumentService = Depends(get_document_service)):
    return await service.get_all_documents()
