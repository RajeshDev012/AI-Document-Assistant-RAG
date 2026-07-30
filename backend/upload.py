from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from rag import extract_text, split_text, store_chunks

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text(file_path)

        chunks = split_text(text)

        store_chunks(chunks, file.filename)

        return {
            "filename": file.filename,
            "message": "PDF uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))