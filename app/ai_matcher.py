import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_match_score(user_skills: list, job_tags: list, job_description: str = "") -> float:
    """
    Compute a match score between a user's skills and a job's requirements.
    Returns a float between 0 and 100.
    """
    if not user_skills or not job_tags:
        return 0.0

    user_text = " ".join(user_skills).lower()
    job_text = " ".join(job_tags).lower() + " " + (job_description or "").lower()

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([user_text, job_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 1)
    except Exception:
        # Fallback: simple keyword overlap
        user_set = set(user_skills)
        job_set = set(job_tags)
        overlap = len(user_set & job_set)
        total = len(user_set | job_set)
        return round((overlap / total * 100) if total else 0.0, 1)


def get_recommended_jobs(user_skills: list, jobs: list, top_n: int = 5) -> list:
    """
    Return top_n jobs sorted by match score descending.
    Each element: (job, score)
    """
    scored = []
    for job in jobs:
        tags = job.get_tags()
        score = compute_match_score(user_skills, tags, job.description or "")
        scored.append((job, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
