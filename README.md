# AI_Workspace_Platform

A production-style Retrieval-Augmented Generation (RAG) platform designed to evaluate AI reliability through grounding checks, hallucination detection, retrieval quality scoring, and automated evaluation metrics.

Unlike basic RAG systems, this platform measures whether generated answers are trustworthy and grounded in retrieved context.

---

# Features

- PDF document ingestion
- Semantic retrieval using embeddings
- Context-aware question answering
- Hallucination detection
- Groundedness scoring
- Retrieval quality metrics
- Latency tracking
- FastAPI backend
- Streamlit frontend
- Automated evaluation pipeline

---

# Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn

## AI / Retrieval

- OpenAI APIs
- Embeddings
- Retrieval-Augmented Generation (RAG)
- Vector Similarity Search

## Evaluation

- Hallucination Detection
- Groundedness Scoring
- Retrieval Metrics
- Keyword Accuracy Checks

## Frontend

- Streamlit

---

# Project Structure

```text
rag-evaluation-platform/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── frontend/
│   └── frontend.py
│
├── rag/
│   ├── indexer.py
│   └── retriever.py
│
├── eval/
│   ├── evaluator.py
│   └── test_cases.json
│
├── screenshots/
│   ├── img1.png
│   └── img2.png
```

---

# Screenshots

## Upload + Question Answering

![UI](screenshots/img1.png)

## Evaluation Metrics

![Metrics](screenshots/img2.png)

---

# How It Works

```text
User Question
      ↓
Embedding Generation
      ↓
Vector Retrieval
      ↓
Top-K Chunks
      ↓
LLM Answer Generation
      ↓
Evaluation Pipeline
      ↓
Grounding + Hallucination Checks
```

---

# Evaluation Metrics

The system automatically computes:

- Groundedness Score
- Hallucination Risk
- Retrieval Similarity
- Latency
- Keyword Accuracy

Example:

```json
{
  "groundedness_score": 0.333,
  "hallucination_risk": "MEDIUM",
  "latency_seconds": 3.35
}
```

---

# Installation

Clone:

```bash
git clone YOUR_REPO_URL
cd rag-evaluation-platform
```

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Setup API Key

Create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=your_key_here
```

---

# Run Backend

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Run Frontend

New terminal:

```bash
source venv/bin/activate
streamlit run frontend/frontend.py
```

Frontend:

```text
http://localhost:8501
```

---

# Future Improvements

- Hybrid Search
- Metadata Filtering
- LLM-as-Judge Evaluation
- Prompt Evaluation
- Multi-document Support
- Reranking Pipelines
- Docker Deployment

---

# Resume Description

Built a production-style RAG Evaluation Platform using FastAPI, Streamlit, and OpenAI APIs with hallucination detection, grounding checks, retrieval quality scoring, and automated reliability evaluation workflows.
