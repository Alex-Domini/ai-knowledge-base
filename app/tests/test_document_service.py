import pytest
from datetime import datetime

from app.models.document import Document
from app.services.document_service import DocumentService

CREATED_AT = datetime.fromisoformat("2026-06-18T09:40:44.678Z")


class FakeDocumentRepository:
    def __init__(self) -> None:
        self.save_filename: str | None = None

    async def create(self, filename: str) -> Document:
        self.save_filename = filename
        return Document(filename=filename)

    async def get_all_documents(self) -> list[Document]:
        return [
            Document(
                id=1,
                filename="contract.pdf",
                created_at=CREATED_AT,
            )
        ]


@pytest.mark.asyncio
async def test_create_document_and_normalize():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(repository=fake_repository)

    await service.create_document(" ConTract.PDF ")

    assert fake_repository.save_filename == "contract.pdf"


@pytest.mark.asyncio
async def test_get_all_documents():
    fake_repository = FakeDocumentRepository()
    service = DocumentService(fake_repository)

    documents = await service.get_all_documents()

    assert len(documents) == 1
    assert documents[0].id == 1
    assert documents[0].filename == "contract.pdf"
    assert documents[0].created_at == CREATED_AT
