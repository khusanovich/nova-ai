import fitz  # PyMuPDF
import pdfplumber
import re

class PDFDocument:
    def __init__(self, file, filename):
        self.filename = filename
        self.pages = []

        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page_num, page in enumerate(doc):
            self.pages.append({
                "page_number": page_num + 1,
                "text": page.get_text()
            })
        doc.close()

def extract_text_tables_and_formulas(pdf_path):
    """
    Extrahiert Text, Tabellen und (rudimentär) Formeln aus PDF.
    Gibt ein Dictionary zurück.
    """
    content = {
        "text": "",
        "tables": [],
        "formulas": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # --- Text extrahieren ---
            text = page.extract_text() or ""
            content["text"] += f"\n\n[Seite {page_num}]\n{text}"

            # --- Tabellen extrahieren ---
            try:
                tables = page.extract_tables()
                for table in tables:
                    table_text = "\n".join([" | ".join([cell or "" for cell in row]) for row in table])
                    content["tables"].append({
                        "page": page_num,
                        "data": table_text
                    })
            except Exception as e:
                print(f"[WARNUNG] Tabelle auf Seite {page_num} konnte nicht extrahiert werden: {e}")

            # --- Formeln (rudimentär) finden ---
            # Heuristik: erkenne z. B. LaTeX-ähnliche oder Gleichungszeichen
            formulas = re.findall(r"[A-Za-z0-9_\^\-\+\*/=<>]+", text)
            formulas = [f for f in formulas if any(sym in f for sym in ["=", "+", "-", "*", "/"])]
            if formulas:
                content["formulas"].append({
                    "page": page_num,
                    "data": formulas
                })

    return content