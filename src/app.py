import os
import tempfile
import streamlit as st

from parse_resumes import extract_text
from embeddings import split_text_into_chunks, get_embedding_model
from vector_store import get_chroma_collection

st.set_page_config(page_title="ResumeRanker AI", page_icon="🧠")

st.title("🧠 ResumeRanker AI")
st.write("AI-powered resume screening and ranking system.")

embedding_model = get_embedding_model()
collection = get_chroma_collection()

# ---------------- Job Description ----------------
st.subheader("Step 1: Enter Job Description")
job_desc = st.text_area("Paste job description here", height=200)

# ---------------- Resume Upload ------------------
st.subheader("Step 2: Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload resumes (PDF / DOCX / TXT)",
    type=["pdf", "docx", "doc", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resume(s) uploaded")

    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.getbuffer())
            path = tmp.name

        text = extract_text(path)
        chunks = split_text_into_chunks(text)

        for chunk in chunks:
            collection.add(
                documents=[chunk],
                metadatas=[{"filename": file.name}],
                ids=[f"{file.name}_{hash(chunk)}"],
                embeddings=[embedding_model.embed_query(chunk)]
            )

        os.remove(path)

    st.success("✅ Resumes indexed into Vector Database")

# ---------------- AI Ranking ------------------
if st.button("Rank Resumes"):
    if not job_desc:
        st.error("Please enter a job description")
    else:
        results = collection.query(
            query_embeddings=[embedding_model.embed_query(job_desc)],
            n_results=5
        )

        st.subheader("📊 Ranking Results")
        for i, meta in enumerate(results["metadatas"][0]):
            st.write(f"{i+1}. 📄 {meta['filename']}")
