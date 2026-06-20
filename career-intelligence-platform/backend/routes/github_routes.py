from flask import Blueprint
from flask import request
from flask import jsonify

from ai.github_analyzer import analyze_github

github_bp = Blueprint(
    'github',
    __name__
)


@github_bp.route(
    '/analyze',
    methods=['POST']
)
def github_analysis():

    try:

        data = request.get_json()

        username = data.get(
            'username'
        )

        if not username:

            return jsonify({
                'error':
                'GitHub username is required'
            }), 400

        result = analyze_github(
            username
        )

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'error': str(e)
        }), 500