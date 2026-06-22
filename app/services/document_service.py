from typing import Protocol
from app.models.document import Document


class DocumentRepositoryProtocol(Protocol):
    async def create(self, filename: str) -> Document: ...

    async def get_all_documents(self) -> list[Document]: ...

    async def get_document_by_id(self, document_id: int) -> Document | None: ...

    async def delete_document_by_id(self, document_id: int) -> Document | None: ...


class DocumentService:
    def __init__(self, repository: DocumentRepositoryProtocol) -> None:
        self.repository = repository

    async def create_document(self, filename: str) -> Document:
        normalized_filename = filename.strip().lower()

        if not normalized_filename:
            raise ValueError("Filename cannot be empty")
        document = await self.repository.create(filename=normalized_filename)

        return document

    async def get_all_documents(self) -> list[Document]:
        documents = await self.repository.get_all_documents()
        return documents

    async def get_document_by_id(self, document_id: int) -> Document | None:
        document = await self.repository.get_document_by_id(document_id)
        return document

    async def delete_document_by_id(self, document_id: int) -> Document | None:
        document = await self.repository.delete_document_by_id(document_id)
        return document
