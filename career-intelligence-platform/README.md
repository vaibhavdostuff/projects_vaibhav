# Career Intelligence Platform

An AI-powered platform that helps users:

- Analyze resumes
- Calculate ATS scores
- Predict suitable career roles
- Generate interview questions
- Build learning roadmaps
- Analyze GitHub profiles
- Recommend jobs

---

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Axios
- React Router

### Backend

- Flask
- SQLAlchemy
- JWT Authentication
- Flask-CORS

### AI / ML

- OpenAI GPT
- Sentence Transformers
- Scikit-Learn
- Random Forest

---

## Installation

### Clone Project

```bash
git clone <repository_url>

cd career-intelligence-platform
```

### Backend Setup

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

Backend runs on:

```plaintext
http://localhost:5000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```plaintext
http://localhost:5173
```

---

## Main Features

### Resume Analysis

- PDF Resume Upload
- Skill Extraction
- ATS Score Generation

### Career Prediction

- ML Based Role Prediction
- Skill Matching

### Job Recommendation

- Semantic Matching
- Similarity Scoring

### Interview Preparation

- AI Generated Questions
- Beginner to Advanced Levels

### GitHub Analysis

- Repository Count
- Stars
- Languages Used

### Roadmap Generator

- 6 Month Learning Plans
- Personalized Career Paths

---

## Environment Variables

Create `.env`

```env
OPENAI_API_KEY=YOUR_KEY

JWT_SECRET_KEY=YOUR_SECRET

DATABASE_URL=sqlite:///career.db
```

---

## Folder Structure

```plaintext
career-intelligence-platform

backend/
frontend/
README.md
.gitignore
```