from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.gemini_service import format_liturgy_text
from fastapi import FastAPI, UploadFile, File, HTTPException
import docx
import io

app = FastAPI()

# middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LiturgyRequest(BaseModel):
    text: str

@app.post("/format")
async def process_liturgy(request: LiturgyRequest):
    formatted_result = format_liturgy_text(request.text)
    return {"formatted_text": formatted_result}

@app.post("/format-file")
async def process_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = ""

    if filename.endswith('.docx') or filename.endswith('.doc'):
        # Baca file Word
        file_bytes = await file.read()
        doc = docx.Document(io.BytesIO(file_bytes))
        content = "\n".join([para.text for para in doc.paragraphs])
    
    else:
        return {"error": "Format file gak didukung, King!"}

    formatted_result = format_liturgy_text(content)
    return {"formatted_text": formatted_result}