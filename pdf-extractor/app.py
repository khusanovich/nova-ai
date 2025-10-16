import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- PDF Text Extraktion ---
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- Frage beantworten ---
def answer_question(text, question):
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]

    if not paragraphs:
        return "Kein relevanter Text gefunden."

    docs = paragraphs + [question]
    vectorizer = TfidfVectorizer().fit_transform(docs)
    similarities = cosine_similarity(vectorizer[-1], vectorizer[:-1]).flatten()

    best_match_index = similarities.argmax()
    best_paragraph = paragraphs[best_match_index]
    return f"🔍 Relevanteste Textstelle:\n\n{best_paragraph}"

# --- Streamlit UI ---
st.title("📘 Offline PDF-Q&A Tool")
uploaded_file = st.file_uploader("Lade eine PDF hoch", type=["pdf"])

if uploaded_file:
    with st.spinner("Extrahiere Text..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    st.success("Text erfolgreich extrahiert ✅")

    question = st.text_input("Frage zum Inhalt der PDF:")
    if question:
        answer = answer_question(pdf_text, question)
        st.markdown(answer)
