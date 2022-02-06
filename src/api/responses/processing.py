from pydantic import BaseModel


class ProcessingStatus(BaseModel):
    id: int
    pages: int
    status: str
