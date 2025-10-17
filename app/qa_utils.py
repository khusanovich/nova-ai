from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_best_answer(pdfs, question, top_n=3):
    all_paragraphs = []
    mapping = []

    for pdf in pdfs:
        for page in pdf.pages:
            paragraphs = [p.strip() for p in page["text"].split("\n") if len(p.strip()) > 20]
            all_paragraphs.extend(paragraphs)
            mapping.extend([{"pdf": pdf.filename, "page": page["page_number"]}] * len(paragraphs))

    if not all_paragraphs:
        return []

    vectorizer = TfidfVectorizer().fit([question] + all_paragraphs)
    vectors = vectorizer.transform([question] + all_paragraphs)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "pdf": mapping[idx]["pdf"],
            "page": mapping[idx]["page"],
            "context": all_paragraphs[idx],
            "score": float(similarities[idx])
        })
    return results
