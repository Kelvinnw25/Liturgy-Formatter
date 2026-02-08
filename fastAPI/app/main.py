from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.gemini_service import format_liturgy_text
from fastapi import FastAPI, UploadFile, File, HTTPException
import docx
import io

app = FastAPI()

# Middleware CORS - Izinkan semua biar aman di cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LiturgyRequest(BaseModel):
    text: str

# TAMBAHKAN /api di depan rute
@app.post("/api/format") 
async def process_liturgy(request: LiturgyRequest):
    formatted_result = format_liturgy_text(request.text)
    return {"formatted_text": formatted_result}

# TAMBAHKAN /api di depan rute
@app.post("/api/format-file")
async def process_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = ""

    if filename.endswith('.docx') or filename.endswith('.doc'):
        file_bytes = await file.read()
        doc = docx.Document(io.BytesIO(file_bytes))
        content = "\n".join([para.text for para in doc.paragraphs])
    else:
        return {"error": "Format file gak didukung, King!"}

    formatted_result = format_liturgy_text(content)
    return {"formatted_text": formatted_result}