import os
import shutil
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from pdf_utils import extract_text_from_pdf
from database import init_db, add_pdf_metadata, get_pdf_by_id
from langchain_service import get_answer  # Async function to get answer

# Load environment variables
load_dotenv()

# FastAPI setup
app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory setup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize SQLite DB
init_db()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(file_path)
    doc_id = add_pdf_metadata(file.filename, text)
    return {"message": "Uploaded", "doc_id": doc_id}

@app.post("/ask/")
async def ask_question(doc_id: int = Form(...), question: str = Form(...)):
    doc = get_pdf_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Await the async answer function here
    answer = await get_answer(doc["text"], question)
    return {"answer": answer}
