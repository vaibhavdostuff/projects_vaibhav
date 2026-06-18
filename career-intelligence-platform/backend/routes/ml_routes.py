from flask import Blueprint
from flask import request
from flask import jsonify

import os
import joblib

ml_bp = Blueprint(
    'ml',
    __name__
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    'ml',
    'career_model.pkl'
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}"
    )

model = joblib.load(
    MODEL_PATH
)


@ml_bp.route(
    '/predict_role',
    methods=['POST']
)
def predict_role():

    try:

        data = request.get_json()

        resume_text = data.get(
            'resume_text'
        )

        if not resume_text:

            return jsonify({
                'success': False,
                'error': 'resume_text is required'
            }), 400

        prediction = model.predict(
            [resume_text]
        )[0]

        return jsonify({
            'success': True,
            'predicted_role': prediction
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500