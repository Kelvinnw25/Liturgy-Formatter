from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import docx
import io
import os
from dotenv import load_dotenv

#gemini api key setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

#middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LiturgyRequest(BaseModel):
    text: str

#logic function to format liturgy text
def format_liturgy_logic(raw_text):
    model = genai.GenerativeModel('gemini-2.5-flash') 
    prompt = f"""
    Tugas: Rapikan teks liturgi berikut ke dalam format EasyWorship.
    
    Strict Rules:
    1. Gunakan HANYA lirik yang ada di input. Jangan menambah lirik dari luar.
    2. Berikan label [Verse 1], [Chorus], [Coda], dll secara jelas.
    3. JANGAN PERNAH memberikan penjelasan, saran, atau komentar apapun.
    4. JANGAN PERNAH curhat kalau teks tidak jelas.
    5. JIKA teks input adalah sampah/ngasal, cukup balas dengan: [Verse 1] (isi teks ngasal tadi).
    6. HANYA keluarkan output teks hasil format.
    7. Ikuti format persis seperti contoh ini (perhatikan juga enter spasi dan baris kosongnya):
    KJ 3 - Kami Puji Dengan Riang
    (blank line)
    (blank line)
    Verse 1
    Lirik...
    (blank line)
    Lirik...
    (blank line)
    Lirik...
    (blank line)
    (blank line)
    Chorus
    Lirik...
    (blank line)
    Lirik...
    (blank line)
    Lirik...
    (blank line)
    (blank line)
    (blank line)
    (blank line)
    Teks Input:
    {raw_text}
    """
    response = model.generate_content(prompt)
    return response.text

#endpoint to process liturgy text
@app.post("/api/format") #prefix /api should be used
async def process_liturgy(request: LiturgyRequest):
    try:
        result = format_liturgy_logic(request.text)
        return {"formatted_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/format-file") #prefix /api should be used
async def process_file(file: UploadFile = File(...)):
    if not (file.filename.lower().endswith('.docx') or file.filename.lower().endswith('.doc')):
        return {"error": "Format file gak didukung, King!"}
    
    try:
        file_bytes = await file.read()
        doc = docx.Document(io.BytesIO(file_bytes))
        content = "\n".join([para.text for para in doc.paragraphs])
        result = format_liturgy_logic(content)
        return {"formatted_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))