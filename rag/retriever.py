import json
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INDEX_PATH = "uploads/index.json"


def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def load_index():
    if not os.path.exists(INDEX_PATH):
        return []

    with open(INDEX_PATH, "r") as f:
        return json.load(f)


def retrieve_chunks(query: str, top_k: int = 4):
    index = load_index()

    if not index:
        return []

    query_embedding = get_embedding(query)

    scored_chunks = []

    for item in index:
        score = cosine_similarity(query_embedding, item["embedding"])

        scored_chunks.append({
            "text": item["text"],
            "metadata": item["metadata"],
            "score": round(score, 4)
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]
