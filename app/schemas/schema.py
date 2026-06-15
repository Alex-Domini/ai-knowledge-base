from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DocumentCreate(BaseModel):
    filename: str
    model_config = ConfigDict(from_attributes=True)


class DocumentRead(BaseModel):
    id: int
    filename: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
