from flask import Blueprint, request, jsonify
import joblib
import os

ml_bp = Blueprint('ml', __name__)

# ✅ FIX 2: Use absolute path to load the model.
#    Old code used 'ml/career_model.pkl' (relative to CWD).
#    This breaks whenever the server is not run from backend/ directory.
#    __file__ is routes/ml_routes.py, so we go up one level to backend/
#    then into ml/career_model.pkl.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "career_model.pkl")

# ✅ FIX 3: Load lazily on first request instead of crashing at import time.
#    Old code called joblib.load() at module level — if the file is missing
#    the entire app fails to start. Now we load on first use and give a
#    clean 503 error instead of a startup crash.
_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                f"Run train_model.py first to generate it."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


@ml_bp.route('/predict_role', methods=['POST'])
def predict_role():
    try:
        model = get_model()
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 503

    data = request.json
    resume_text = data.get('resume_text', '')

    if not resume_text:
        return jsonify({'error': 'resume_text is required'}), 400

    prediction = model.predict([resume_text])[0]

    return jsonify({
        'predicted_role': prediction
    })
