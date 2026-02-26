import shutil

from pathlib import Path

from fastapi import APIRouter, UploadFile, File
from services.file_converter import FileConverter

legislation_router = APIRouter()
processor = FileConverter()

@legislation_router.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):

    temp_path = Path(f'storage/{file.filename}')
    temp_path.parent.mkdir(exist_ok=True)

    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    markdown_text = processor.pdf_to_markdown(str(temp_path))

    temp_path.unlink()

    return {"markdown": markdown_text}
