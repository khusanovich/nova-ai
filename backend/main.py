from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.pdf_document import extract_text_tables_and_formulas
from app.qa_utils import answer_question


app = FastAPI(title="PDF Chatbot")

# Frontend Ordner mounten
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Root zeigt direkt das Chat-Frontend
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

# Speicher für hochgeladene PDFs
pdf_storage = []

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf = PDFDocument(file.file, file.filename)
    pdf_storage.append(pdf)
    return {"message": f"{file.filename} uploaded", "pages": len(pdf.pages)}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    if not pdf_storage:
        return {"error": "No PDFs uploaded yet."}
    answers = find_best_answer(pdf_storage, question)
    return {"question": question, "answers": answers}

@app.get("/documents")
async def list_docs():
    return [{"filename": pdf.filename, "pages": len(pdf.pages)} for pdf in pdf_storage]
