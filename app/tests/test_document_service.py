import pytest
from datetime import datetime

from app.models.document import Document
from app.services.document_service import DocumentService

CREATED_AT = datetime.fromisoformat("2026-06-18T09:40:44.678Z")


class FakeDocumentRepository:
    def __init__(self) -> None:
        self.save_filename: str | None = None
        self.documents = [
            Document(
                id=1,
                filename="contract.pdf",
                created_at=CREATED_AT,
            )
        ]

    async def create(self, filename: str, text_content: str) -> Document:
        self.save_filename = filename
        self.saved_some_content = text_content
        return Document(filename=filename)

    async def get_all_documents(self) -> list[Document]:
        return self.documents

    async def get_document_by_id(self, document_id: int) -> Document | None:
        return Document(id=document_id, filename="contract.pdf", created_at=CREATED_AT)

    async def delete_document_by_id(self, document_id: int) -> Document | None:
        for document in self.documents:
            if document.id == document_id:
                self.documents.remove(document)
                return document
        return None


@pytest.mark.asyncio
async def test_create_document_and_normalize():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(repository=fake_repository)

    await service.create_document(" ConTract.PDF ", "Some text")

    assert fake_repository.save_filename == "contract.pdf"
    assert fake_repository.saved_some_content == "Some text"


@pytest.mark.asyncio
async def test_get_all_documents():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    documents = await service.get_all_documents()

    assert len(documents) == 1
    assert documents[0].id == 1
    assert documents[0].filename == "contract.pdf"
    assert documents[0].created_at == CREATED_AT


@pytest.mark.asyncio
async def test_get_document_by_id():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    document = await service.get_document_by_id(1)

    assert document is not None
    assert document.id == 1


@pytest.mark.asyncio
async def test_get_document_by_id_returns_none_if_not_found():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    document = await service.get_document_by_id(999)

    assert document is not None


@pytest.mark.asyncio
async def test_delete_document_by_id():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    document = await service.delete_document_by_id(1)

    assert document is not None
    assert document.id == 1
    assert len(fake_repository.documents) == 0


@pytest.mark.asyncio
async def test_delete_document_by_id_returns_none_if_not_found():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    document = await service.delete_document_by_id(999)

    assert document is None
