import time


def keyword_accuracy(answer: str, expected_keywords: list):
    answer_lower = answer.lower()
    matched = []

    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            matched.append(keyword)

    score = len(matched) / len(expected_keywords) if expected_keywords else 0

    return {
        "score": round(score, 3),
        "matched_keywords": matched
    }


def groundedness_check(answer: str, retrieved_chunks: list):
    if not retrieved_chunks:
        return {
            "groundedness_score": 0,
            "hallucination_risk": "HIGH"
        }

    answer_words = set(answer.lower().split())
    context_text = " ".join([chunk["text"] for chunk in retrieved_chunks]).lower()
    context_words = set(context_text.split())

    if not answer_words:
        return {
            "groundedness_score": 0,
            "hallucination_risk": "HIGH"
        }

    overlap = len(answer_words.intersection(context_words)) / len(answer_words)

    if overlap < 0.2:
        risk = "HIGH"
    elif overlap < 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "groundedness_score": round(overlap, 3),
        "hallucination_risk": risk
    }


def retrieval_quality(retrieved_chunks: list):
    if not retrieved_chunks:
        return {
            "avg_retrieval_score": 0,
            "top_score": 0
        }

    scores = [chunk["score"] for chunk in retrieved_chunks]

    return {
        "avg_retrieval_score": round(sum(scores) / len(scores), 3),
        "top_score": round(max(scores), 3)
    }


def evaluate_response(answer: str, retrieved_chunks: list, expected_keywords=None, latency=None):
    if expected_keywords is None:
        expected_keywords = []

    return {
        "keyword_accuracy": keyword_accuracy(answer, expected_keywords),
        "groundedness": groundedness_check(answer, retrieved_chunks),
        "retrieval_quality": retrieval_quality(retrieved_chunks),
        "latency_seconds": latency
    }
