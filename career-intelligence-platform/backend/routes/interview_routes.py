from flask import Blueprint
from flask import request
from flask import jsonify

from ai.interview_question import (
    generate_questions
)

interview_bp = Blueprint(
    'interview',
    __name__
)


@interview_bp.route(
    '/generate',
    methods=['POST']
)
def generate_interview_questions():

    try:

        data = request.get_json()

        role = data.get(
            'role'
        )

        if not role:

            return jsonify({
                'error':
                'Role is required'
            }), 400

        questions = generate_questions(
            role
        )

        return jsonify({
            'success': True,
            'role': role,
            'questions': questions
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500