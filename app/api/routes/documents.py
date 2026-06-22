from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.services.document_service import DocumentService
from app.services.parser_service import ParserService
from app.schemas.schema import DocumentRead
from app.api.dependencies.document import get_document_service

router = APIRouter(prefix="/documents", tags=["AI Knowledge Base"])


@router.post("/upload", response_model=DocumentRead)
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    parser = ParserService()
    filename = file.filename
    if filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )
    content = await file.read()
    text = await parser.parse_txt(content)
    document = await service.create_document(filename, text)
    return document


@router.get("/", response_model=list[DocumentRead])
async def get_all_documents(service: DocumentService = Depends(get_document_service)):
    return await service.get_all_documents()


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document_by_id(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
):
    document = await service.get_document_by_id(document_id)

    if document_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document


@router.delete("/{document_id}", response_model=DocumentRead)
async def delete_document_by_id(
    document_id: int, service: DocumentService = Depends(get_document_service)
):
    document = await service.delete_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document
