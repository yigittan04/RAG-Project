from pathlib import Path
import fitz
from docx import Document

class DocumentLoader:

    @staticmethod
    def load_txt(path: str):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    @staticmethod
    def load_pdf(path: str):
        document = fitz.open(path)

        text = ""

        for page in document:
            text += page.get_text()
        
        return text
    
    @staticmethod
    def load_docx(path: str):
        document = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )
    
    @staticmethod
    def load(path: str):

        extension = Path(path).suffix.lower()

        if extension == ".txt":
            return DocumentLoader.load_txt(path)
        
        if extension == ".pdf":
            return DocumentLoader.load_pdf(path)
        
        if extension == ".docx":
            return DocumentLoader.load_docx(path)
        
        raise ValueError(f"Unsupported file type: {extension}")