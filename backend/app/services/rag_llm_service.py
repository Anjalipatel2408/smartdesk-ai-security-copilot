import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_rag_answer(query, context_chunks):
    context_text = "\n\n---\n\n".join([c.chunk_text for c in context_chunks])

    prompt = f"""You are SmartDesk AI, a security knowledge assistant. Answer the question
ONLY using the context below. If the answer isn't in the context, say so honestly —
do not make up information.

Context:
{context_text}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content