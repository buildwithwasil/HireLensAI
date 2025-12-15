# src/parse_resumes.py
import os
import pdfplumber
from docx import Document

def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)

def extract_text_from_docx(path: str) -> str:
    """Extract text from a DOCX file."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(path: str) -> str:
    """
    Detect file type from extension and extract text.
    Supports: .pdf, .docx, .doc, .txt
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        # Fallback: try reading as text
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
