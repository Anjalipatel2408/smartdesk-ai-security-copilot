import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.model_router import classify_query_complexity
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from google.genai.errors import ServerError

load_dotenv()

fast_model = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=os.getenv("GOOGLE_API_KEY"))
powerful_model = ChatGoogleGenerativeAI(model="gemini-pro-latest", google_api_key=os.getenv("GOOGLE_API_KEY"))

@retry(
    retry=retry_if_exception_type(ServerError),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(5),
)
def generate_rag_answer(query, context_chunks):
    complexity = classify_query_complexity(query)
    llm = powerful_model if complexity == "complex" else fast_model

    context_text = "\n\n---\n\n".join([c.chunk_text for c in context_chunks])
    prompt = f"""You are SmartDesk AI, a security knowledge assistant. Answer ONLY using
the context below. If not found, say so honestly.

Context:
{context_text}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content, complexity