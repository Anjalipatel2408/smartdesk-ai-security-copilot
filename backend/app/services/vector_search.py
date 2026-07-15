from sqlalchemy import text
from app.services.embedding_service import get_embedding

def search_similar_chunks(db, query, top_k=5):
    query_embedding = get_embedding(query)

    # pgvector cosine distance operator: <=>
    result = db.execute(
        text("""
            SELECT id, document_id, chunk_text,
                   1 - (embedding <=> (:query_embedding)::vector) AS similarity
            FROM document_chunks
            ORDER BY embedding <=> (:query_embedding)::vector
            LIMIT :top_k
        """),
        {"query_embedding": str(query_embedding), "top_k": top_k}
    )
    return result.fetchall()