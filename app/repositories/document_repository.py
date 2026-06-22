from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, filename: str) -> Document:
        file_obj = Document(filename=filename)
        self.session.add(file_obj)
        await self.session.commit()
        await self.session.refresh(file_obj)
        return file_obj

    async def get_all_documents(self) -> list[Document]:
        result = await self.session.execute(select(Document))
        return list(result.scalars().all())

    async def check_connection(self) -> dict:
        await self.session.execute(text("SELECT 1"))
        return {"status": "database connected"}

    async def get_document_by_id(self, document_id: int) -> Document | None:
        document = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        return document.scalar_one_or_none()

    async def delete_document_by_id(self, document_id: int) -> Document | None:
        query = select(Document).where(Document.id == document_id)
        result = await self.session.execute(query)
        document = result.scalar_one_or_none()

        if document is None:
            return None

        await self.session.delete(document)
        await self.session.commit()
        return document
