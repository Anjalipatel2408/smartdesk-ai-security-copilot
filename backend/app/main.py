from fastapi import FastAPI
from app.database import engine
from app.database import engine
from app.database import Base, engine
from app.models.document_model import Document
from app.routes.document_routes import router as document_router
from app.models.chunk_model import DocumentChunk

app = FastAPI(title="SmartDesk AI — Security Intelligence Copilot")

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "SmartDesk AI"}




@app.get("/test-db")
def test_db():
    try:
        conn = engine.connect()
        conn.close()
        return {"database": "Connected successfully!"}
    except Exception as e:
        return {"database": "Failed", "error": str(e)}
    
Base.metadata.create_all(bind=engine)
app.include_router(document_router)