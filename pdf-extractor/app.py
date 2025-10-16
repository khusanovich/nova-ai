import streamlit as st
from extract_utils import extract_text_from_pdf

st.title("PDF → Text Extractor")

# PDF Upload
uploaded_file = st.file_uploader("Wähle eine PDF-Datei aus", type=["pdf"])

if uploaded_file:
    st.info("PDF wird verarbeitet...")
    text = extract_text_from_pdf(uploaded_file)
    
    # Ergebnis anzeigen
    st.subheader("Extrahierter Text")
    st.text_area("Text", text, height=400)
    
    # Optional: Text speichern
    if st.button("Als .txt speichern"):
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        st.success("Text als output.txt gespeichert")
