'use client';
import { useState, useRef } from 'react';

export default function LiturgyPage() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  //function to handle file upload and read content
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const res = await fetch('/api/format-file', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        //catch specific errors
        if (res.status === 404) throw new Error("Endpoint gak ketemu! Cek lagi vercel.json lo.");
        if (res.status === 500) throw new Error("Server AI lagi pusing (Error 500). Cek Runtime Logs di Vercel.");
        throw new Error(`Error: ${res.statusText}`);
      }

      const data = await res.json();
      if (data.formatted_text) {
        setOutput(data.formatted_text);
      } else {
        alert(`Waduh: ${data.error || 'Gagal dapet hasil format.'}`);
      }
    } catch (err: any) {
      alert(`Gagal Upload: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  //function to call FastAPI endpoint for formatting
  const handleFormat = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/format', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
      });

      if (!res.ok) {
        throw new Error(`Server ngasih error ${res.status}. Kemungkinan API Key Gemini bermasalah.`);
      }

      const data = await res.json();
      setOutput(data.formatted_text);
    } catch (err: any) {
      alert(`Gagal Format: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  //function to download output as .txt file
  const downloadResult = () => {
    if (!output) return;
    const element = document.createElement("a");
    const file = new Blob([output], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "lagu korem.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <main className="min-h-screen bg-slate-50 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-extrabold text-slate-900">⛪ Liturgy Formatter</h1>
          <p className="text-slate-500">Yang Waha Waha aja</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* input column */}
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <label className="font-bold text-slate-700">Input (Liturgy)</label>
              {/* upload file button */}
              <button 
                onClick={() => fileInputRef.current?.click()}
                className="text-sm bg-green-100 text-green-700 hover:bg-green-200 px-3 py-1 rounded-md font-semibold transition-colors"
              >
                📁 Upload File .docx
              </button>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileUpload} 
                accept=".docx, .doc"
                className="hidden" 
              />
            </div>
            <textarea
              className="h-[500px] p-4 border-2 border-slate-200 rounded-2xl bg-white text-slate-800 shadow-inner focus:border-blue-500 outline-none transition-all resize-none"
              placeholder="Paste seluruh isi liturgi di sini atau upload file .docx..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>
          
          {/* output column */}
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <label className="font-bold text-slate-700">Output (Format EasyWorship)</label>
              {/* download button */}
              {output && (
                <button 
                  onClick={downloadResult}
                  className="text-sm bg-green-100 text-green-700 hover:bg-green-200 px-3 py-1 rounded-md font-semibold transition-colors"
                >
                  📁 Download .txt
                </button>
              )}
            </div>
            <textarea
              className="h-[500px] p-4 border-2 border-slate-800 rounded-2xl bg-slate-900 text-emerald-400 font-mono shadow-xl resize-none"
              readOnly
              value={output}
              placeholder="Hasilnya bakal muncul di sini..."
            />
          </div>
        </div>

        {/* main button */}
          <button
            onClick={handleFormat}
            disabled={loading || !input}
            className={`w-full py-5 rounded-2xl font-black text-xl transition-all active:scale-[0.98] shadow-xl disabled:cursor-not-allowed text-white
              ${loading 
                ? 'bg-orange-500' //loading (Orange)
                : (input ? 'bg-green-600 hover:bg-green-700' : 'bg-slate-300') //input (green), no input (grey)
              }`}
          >
            {loading ? 'SABAR YEEE...' : 'GASKAN KING!!!'}
          </button>
      </div>
    </main>
  );
}