import pdfplumber

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def find_answer(text, question, max_chars=300):
    """
    Einfache Offline-Fragenbeantwortung:
    - Sucht Absätze, die Wörter aus der Frage enthalten
    - Gibt maximal max_chars zurück
    """
    paragraphs = text.split("\n\n")  # PDF in Absätze splitten
    question_words = set(question.lower().split())
    best_para = ""
    best_score = 0

    for para in paragraphs:
        words = set(para.lower().split())
        score = len(words & question_words)
        if score > best_score:
            best_score = score
            best_para = para

    # Antwort kürzen
    return best_para[:max_chars] + ("..." if len(best_para) > max_chars else "")
