import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def format_liturgy_text(raw_text):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Tugas: Rapikan teks liturgi berikut ke dalam format EasyWorship.
    
    Strict Rules:
    1. Gunakan HANYA lirik yang ada di input. Jangan menambah lirik dari luar.
    2. Berikan label [Verse 1], [Chorus], [Coda], dll secara jelas.
    3. Ikuti format persis seperti contoh ini (perhatikan juga enter spasi dan baris kosongnya):
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