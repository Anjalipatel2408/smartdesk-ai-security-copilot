from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document_model import Document
from app.services.document_service import save_uploaded_document
from app.services.text_extractor import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import get_embedding
from app.models.chunk_model import DocumentChunk
from app.services.vector_search import search_similar_chunks
from app.services.rag_llm_service import generate_rag_answer

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

@router.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    results = search_similar_chunks(db, query)
    return [
        {"chunk_id": r.id, "document_id": r.document_id, "text": r.chunk_text, "similarity": float(r.similarity)}
        for r in results
    ]

@router.get("/ask")
def ask_question(query: str, db: Session = Depends(get_db)):
    top_chunks = search_similar_chunks(db, query, top_k=5)

    if not top_chunks:
        return {"answer": "No relevant documents found. Please upload and process documents first."}

    answer = generate_rag_answer(query, top_chunks)

    return {
        "question": query,
        "answer": answer,
        "sources": [{"document_id": c.document_id, "chunk_id": c.id, "similarity": float(c.similarity)} for c in top_chunks]
    }