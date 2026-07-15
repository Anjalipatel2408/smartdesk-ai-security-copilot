from sqlalchemy import Column, Integer, String, ForeignKey
from pgvector.sqlalchemy import Vector
from app.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    chunk_text = Column(String, nullable=False)
    embedding = Column(Vector(768))   # text-embedding-004 gives 768-dimensional vectors