from fastapi import FastAPI,File, UploadFile
import shutil
from pathlib import Path
from uuid import uuid4

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "okay"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    stored_filename = f"{uuid4()}{Path(file.filename).suffix}"

    with open(f"uploaded_files/{stored_filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": stored_filename,
        "message": "PDF uploaded successfully"  ,
        "content_type": file.content_type
        }