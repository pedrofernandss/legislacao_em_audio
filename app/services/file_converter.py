import pymupdf.layout
import pymupdf4llm
from pathlib import Path

class FileConverter:
    def __init__(self, temp_storage: str = "storage/temp"):
        self.temp_storage = Path(temp_storage)
        self.temp_storage.mkdir(parents=True, exist_ok=True)

    def pdf_to_markdown(self, pdf_path: str):
        doc = pymupdf.open(pdf_path)

        return pymupdf4llm.to_markdown(doc)