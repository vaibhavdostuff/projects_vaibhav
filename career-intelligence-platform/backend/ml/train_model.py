import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv(
    'ml/datasets/resume_dataset.csv'
)

X = df['resume_text']
y = df['role']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = Pipeline([
    (
        'tfidf',
        TfidfVectorizer(
            stop_words='english'
        )
    ),
    (
        'classifier',
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    )
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f'Accuracy: {accuracy:.2f}')

joblib.dump(
    model,
    'ml/career_model.pkl'
)

print('Model Saved Successfully')