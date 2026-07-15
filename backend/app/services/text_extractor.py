from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif file_path.lower().endswith(".docx"):
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:  # .txt
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()