from pydantic import BaseModel

from .db.models import ProcessingStatus


class Document(BaseModel):
    id: int
    processing_status: ProcessingStatus
    pages_count: int
    file_path: str

    class Config:
        orm_mode = True


class ProcessedImage(BaseModel):
    document_id: int
    page_number: int
    file_path: str

    class Config:
        orm_mode = True
