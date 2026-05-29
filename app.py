import os
import time
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from rag.indexer import build_index
from rag.retriever import retrieve_chunks
from eval.evaluator import evaluate_response

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Production RAG Evaluation Platform")

UPLOAD_PATH = "uploads/uploaded.pdf"


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "RAG Evaluation Platform is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    contents = await file.read()

    with open(UPLOAD_PATH, "wb") as f:
        f.write(contents)

    result = build_index(UPLOAD_PATH)

    return {
        "filename": file.filename,
        **result
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    start_time = time.time()

    chunks = retrieve_chunks(request.question, top_k=4)

    if not chunks:
        return {
            "answer": "No document uploaded or indexed yet.",
            "sources": [],
            "evaluation": {}
        }

    context = "\n\n".join([chunk["text"] for chunk in chunks])

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a RAG assistant. Answer only using the provided context. "
                    "If the answer is not in the context, say: I could not find that in the document."
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{request.question}"
            }
        ]
    )

    answer = response.output_text
    latency = round(time.time() - start_time, 3)

    evaluation = evaluate_response(
        answer=answer,
        retrieved_chunks=chunks,
        expected_keywords=[],
        latency=latency
    )

    return {
        "answer": answer,
        "sources": chunks,
        "evaluation": evaluation
    }


@app.post("/evaluate")
def evaluate_question(request: AskRequest):
    result = ask_question(request)
    return result["evaluation"]
