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
