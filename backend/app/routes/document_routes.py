from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document_model import Document
from app.services.document_service import save_uploaded_document
from app.services.text_extractor import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import get_embedding
from app.models.chunk_model import DocumentChunk

router = APIRouter()

@router.post("/upload-document")
def upload_document(file: UploadFile = File(...), doc_type: str = Form("policy"), db: Session = Depends(get_db)):
    file_path, file_size = save_uploaded_document(file)

    doc = Document(
        filename=file.filename,
        file_path=file_path,
        doc_type=doc_type,
        file_size=file_size,
        status="uploaded"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "message": "Document uploaded successfully",
        "document_id": doc.id,
        "filename": doc.filename,
        "doc_type": doc.doc_type
    }

@router.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.post("/process-document/{doc_id}")
def process_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return {"error": "Document not found"}

    raw_text = extract_text(doc.file_path)
    chunks = chunk_text(raw_text)

    for chunk in chunks:
        embedding = get_embedding(chunk)
        db_chunk = DocumentChunk(document_id=doc.id, chunk_text=chunk, embedding=embedding)
        db.add(db_chunk)

    doc.status = "embedded"
    db.commit()

    return {"message": "Document processed", "total_chunks": len(chunks)}