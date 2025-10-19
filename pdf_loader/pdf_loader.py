from langchain.schema import Document
from pypdf import PdfReader

def load_pdf(file_path: str):
    """Read a PDF file and convert each page into a LangChain Document."""
    with open(file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        docs = [Document(page_content=page.extract_text()) for page in reader.pages]
    return docs
