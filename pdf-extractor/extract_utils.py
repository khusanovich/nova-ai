import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extrahiert reinen Text aus einer PDF-Datei.
    """
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
