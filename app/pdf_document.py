import fitz  # PyMuPDF

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
