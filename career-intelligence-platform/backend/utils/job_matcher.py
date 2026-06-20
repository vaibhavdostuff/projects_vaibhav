from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

# ✅ FIX: Absolute path — job_matcher.py is in utils/, so go up one level
#    to backend/, then into ml/datasets/jobs.csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS_PATH = os.path.join(BASE_DIR, "ml", "datasets", "jobs.csv")

# ✅ FIX: Lazy-load both the model and CSV on first request
#    instead of at import time — prevents startup crash if file is missing
_model = None
_jobs = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_jobs():
    global _jobs
    if _jobs is None:
        _jobs = pd.read_csv(JOBS_PATH)
    return _jobs


def recommend_jobs(user_resume):
    model = get_model()
    jobs = get_jobs()

    job_descriptions = jobs['skills'].tolist()

    embeddings = model.encode(job_descriptions)
    user_embedding = model.encode([user_resume])

    scores = cosine_similarity(user_embedding, embeddings)[0]

    jobs = jobs.copy()
    jobs['score'] = scores

    top_jobs = jobs.sort_values(
        by='score',
        ascending=False
    ).head(5)

    return top_jobs.to_dict(orient='records')
