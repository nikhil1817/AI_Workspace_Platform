import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("AI Workspace Framework")

st.write("Upload a PDF, ask questions, and inspect reliability metrics.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    response = requests.post(f"{API_URL}/upload", files=files)

    st.subheader("Upload Result")

    try:
        st.json(response.json())
    except Exception:
        st.error(response.text)

question = st.text_input("Ask a question")

if st.button("Ask"):
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question}
    )

    result = response.json()

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Evaluation Metrics")
    st.json(result["evaluation"])

    st.subheader("Retrieved Sources")

    for i, source in enumerate(result["sources"], 1):
        st.write(f"Source {i}")
        st.write("Similarity Score:", source["score"])
        st.write(source["text"][:1000])
