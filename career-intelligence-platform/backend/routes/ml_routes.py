from flask import Blueprint, request, jsonify
import joblib

ml_bp = Blueprint('ml', __name__)

model = joblib.load('ml/career_model.pkl')

@ml_bp.route('/predict_role', methods=['POST'])
def predict_role():

    data = request.json

    resume_text = data['resume_text']

    prediction = model.predict([resume_text])[0]

    return jsonify({
        'predicted_role': prediction
    })