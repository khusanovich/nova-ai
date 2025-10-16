import streamlit as st
import pdfplumber
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- PDF Text Extraktion ---
def extract_text_from_pdf(file):
    text = ""

    # 1️⃣ pdfplumber Versuch
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                try:
                    page_text = page.extract_text() or ""
                    text += page_text
                except Exception as e:
                    print(f"Fehler bei Seite {page.page_number} mit pdfplumber: {e}")
        if text.strip():
            return text
    except Exception as e:
        print(f"pdfplumber gescheitert: {e}")

    # 2️⃣ fitz Versuch
    try:
        doc = fitz.open(file)
        for page in doc:
            try:
                text += page.get_text("text")
            except Exception as e:
                print(f"Fehler bei Seite {page.number} mit fitz: {e}")
        if text.strip():
            return text
    except Exception as e:
        print(f"fitz gescheitert: {e}")

    return "Kein Text extrahiert – eventuell gescannt oder defekt"

# --- Frage beantworten ---
def answer_question(text, question, top_k=3):
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
    if not paragraphs:
        return "Kein relevanter Text gefunden."

    docs = paragraphs + [question]
    vectorizer = TfidfVectorizer().fit_transform(docs)
    similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    top_paragraphs = [paragraphs[i] for i in top_indices]

    result = "\n\n---\n\n".join(top_paragraphs)
    return f"🔍 Relevante Textstellen:\n\n{result}"

# --- Streamlit UI ---
st.title("📘 Robust Offline PDF-Q&A Tool")

uploaded_file = st.file_uploader("Lade eine PDF hoch", type=["pdf"])

if uploaded_file:
    with st.spinner("Extrahiere Text..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    st.success("Text erfolgreich extrahiert ✅")

    question = st.text_input("Frage zum Inhalt der PDF:")
    if question:
        answer = answer_question(pdf_text, question, top_k=5)  # Top 5 Ergebnisse
        st.markdown(answer)

    # Optional: Text als .txt speichern
    if st.button("Text als .txt speichern"):
        st.download_button("Download Text", pdf_text, file_name="extracted_text.txt")
