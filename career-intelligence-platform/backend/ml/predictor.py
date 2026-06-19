import joblib
import os

# ✅ FIX 2 (same as ml_routes): absolute path so this works from anywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "career_model.pkl")

_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict_role(resume_text):
    model = get_model()
    prediction = model.predict([resume_text])[0]
    return prediction
