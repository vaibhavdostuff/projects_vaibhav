import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ✅ FIX 1: Use absolute paths relative to this script's location
#    Old code used relative paths like 'ml/datasets/resume_dataset.csv'
#    which only works if you run from the backend/ directory.
#    __file__ always points to train_model.py itself, so paths are
#    correct regardless of where you run the script from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "resume_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Features and target
X = df["resume_text"]
y = df["role"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Build model pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english"
        )
    ),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    )
])

# Train model
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, MODEL_PATH)
print(f"Model saved to: {MODEL_PATH}")
