from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document_model import Document
from app.services.document_service import save_uploaded_document

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