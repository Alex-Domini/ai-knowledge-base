from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, repository: DocumentRepository) -> None:
        self.repository = repository

    async def create_document(self, filename: str):
        document = await self.repository.create(filename=filename)
        return document

    async def get_all_documents(self):
        documents = await self.repository.get_all_documents()
        return documents
