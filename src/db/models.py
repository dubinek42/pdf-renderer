from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    processing_status = Column(String, nullable=False)
    pages_count = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)


class ProcessedImage(Base):
    __tablename__ = "processed_image"

    document_id = Column(Integer, ForeignKey("document.id"), primary_key=True)
    page_number = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
