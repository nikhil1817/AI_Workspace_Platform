import os
import json
import numpy as np
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INDEX_PATH = "uploads/index.json"


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"

    return text


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_index(file_path: str):
    text = read_pdf(file_path)

    if not text.strip():
        raise ValueError("No readable text found in PDF.")

    chunks = chunk_text(text)

    data = []

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        data.append({
            "id": i,
            "text": chunk,
            "embedding": embedding,
            "metadata": {
                "source": os.path.basename(file_path),
                "chunk_id": i
            }
        })

    os.makedirs("uploads", exist_ok=True)

    with open(INDEX_PATH, "w") as f:
        json.dump(data, f)

    return {
        "message": "Index created successfully",
        "chunks_created": len(chunks)
    }
