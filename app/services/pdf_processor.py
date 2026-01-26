import pymupdf4llm
from pathlib import Path

class PDFProcessor:
    def __init__(self, temp_storage: str = "storage/temp"):
        self.temp_storage = Path(temp_storage)
        self.temp_storage.mkdir(parents=True, exist_ok=True)

    def to_markdown(self, pdf_path: str) -> str:

        return pymupdf4llm.to_markdown(pdf_path)