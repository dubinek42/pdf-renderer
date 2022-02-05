from pydantic import BaseModel


class Document(BaseModel):
    id: int
    processing_status: str
    pages_count: int
    file_path: str

    class Config:
        orm_mode = True
