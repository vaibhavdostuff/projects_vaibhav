from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

jobs = pd.read_csv('datasets/jobs.csv')


def recommend_jobs(user_resume):

    job_descriptions = jobs['skills'].tolist()

    embeddings = model.encode(job_descriptions)

    user_embedding = model.encode([user_resume])

    scores = cosine_similarity(user_embedding, embeddings)[0]

    jobs['score'] = scores

    top_jobs = jobs.sort_values(by='score', ascending=False).head(5)

    return top_jobs.to_dict(orient='records')