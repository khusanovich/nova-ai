import streamlit as st
from extract_utils import extract_text_from_pdf, find_answer

st.title("Offline PDF → Q&A Bot")

uploaded_file = st.file_uploader("Wähle eine PDF-Datei aus", type=["pdf"])

if uploaded_file:
    st.info("PDF wird verarbeitet...")
    text = extract_text_from_pdf(uploaded_file)
    st.success("PDF erfolgreich gelesen!")

    st.subheader("Extrahierter Text")
    st.text_area("Text", text, height=300)

    # Q&A
    question = st.text_input("Stelle eine Frage zum PDF-Inhalt:")
    if question:
        answer = find_answer(text, question)
        st.subheader("Antwort")
        st.write(answer)
