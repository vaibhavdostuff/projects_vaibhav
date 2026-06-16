from flask import Blueprint
from flask import request
from flask import jsonify

from ai.roadmap_generator import (
    generate_roadmap
)

roadmap_bp = Blueprint(
    'roadmap',
    __name__
)


@roadmap_bp.route(
    '/generate',
    methods=['POST']
)
def roadmap():

    try:

        data = request.get_json()

        skills = data.get(
            'skills'
        )

        role = data.get(
            'role'
        )

        if not role:

            return jsonify({
                'error':
                'Target role is required'
            }), 400

        roadmap_result = generate_roadmap(
            skills,
            role
        )

        return jsonify({
            'success': True,
            'role': role,
            'roadmap': roadmap_result
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500