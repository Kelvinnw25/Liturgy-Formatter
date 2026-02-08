# ⛪ Liturgy Formatter

An AI-powered automation tool designed for church multimedia teams to instantly format liturgy text for **EasyWorship**. This project uses **Google Gemini 2.5 Flash** to transform raw lyrics or Word documents into structured slides.

---

## 🛠️ Tech Stack

* **Frontend**: Next.js 15 (App Router), Tailwind CSS, TypeScript.
* **Backend**: FastAPI (Python 3.13), Uvicorn.
* **AI Engine**: Google GenAI SDK (Gemini 2.5 Flash).
* **Document Parsing**: `python-docx` for `.docx` support.

---

## 📂 Project Structure

Based on the current development environment:

```text
LITURGY-FORMATTER/
├── fastAPI/                # Python Backend
│   ├── app/
│   │   ├── core/           # Core configurations
│   │   ├── schemas/        # Pydantic data models
│   │   ├── services/       
│   │   │   └── gemini_service.py  # AI Logic
│   │   └── main.py         # API Endpoints
│   ├── .env                # API Keys (Private)
│   └── requirements.txt    # Python dependencies
├── react/                  # Next.js Frontend
│   ├── app/                # Main Application Pages
│   │   ├── layout.tsx      # Global layout
│   │   └── page.tsx        # UI Logic (The "Gaskan" Page)
│   ├── public/             # Static assets (icons/logos)
│   ├── next.config.ts      # Next.js configuration
│   └── package.json        # Frontend dependencies
├── samples/                # Sample liturgy files for testing
└── README.md

```

---

## 🚀 Getting Started

### 1. Backend Environment Setup

Navigate to the `fastAPI` folder and start the server:

```bash
cd fastAPI
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

```

*The backend runs on `http://localhost:8000`.*

### 2. Frontend Development Setup

Open a new terminal, navigate to the `react` folder, and start the development server:

```bash
cd react
npm install
npm run dev

```

*The frontend runs on `http://localhost:3000`.*

---

## 🔑 Configuration

Create a `.env` file inside the `fastAPI/` directory:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key

```

> **Warning**: Do not upload your `.env` file to GitHub. It is already included in the `.gitignore`.

---

## 📝 Features

* **AI Formatting**: Automatically identifies Verse, Chorus, and Bridge.
* **File Upload**: Supports extraction from `.docx` files.
* **Export**: Download results as `.txt` for direct use in EasyWorship.
* **Responsive UI**: Optimized for quick usage during church service prep.

---

### How to use this:

1. Open your `README.md` in VS Code.
2. Select all and delete.
3. Paste this version and save (**Ctrl + S**).