import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


df = pd.read_csv('datasets/resume_dataset.csv')

X = df['resume_text']
y = df['role']

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', RandomForestClassifier())
])

model.fit(X_train, y_train)

joblib.dump(model, 'career_model.pkl')

print('Model Trained')