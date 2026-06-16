from app.repositories.document_repository import DocumentRepository
from app.models.document import Document


class DocumentService:
    def __init__(self, repository: DocumentRepository) -> None:
        self.repository = repository

    async def create_document(self, filename: str) -> Document:
        normalized_filename = filename.strip().lower()
        document = await self.repository.create(filename=normalized_filename)
        return document

    async def get_all_documents(self) -> list[Document]:
        documents = await self.repository.get_all_documents()
        return documents
