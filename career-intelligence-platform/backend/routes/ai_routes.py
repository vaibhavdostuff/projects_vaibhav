from flask import Blueprint, request, jsonify

from ai.interview_generator import generate_questions
from ai.roadmap_generator import generate_roadmap
from ai.github_analyzer import analyze_github

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/interview', methods=['POST'])
def interview_questions():

    data = request.json

    result = generate_questions(data['role'])

    return jsonify({
        'questions': result
    })

@ai_bp.route('/roadmap', methods=['POST'])
def roadmap():

    data = request.json

    result = generate_roadmap(
        data['skills'],
        data['role']
    )

    return jsonify({
        'roadmap': result
    })

@ai_bp.route('/github', methods=['POST'])
def github_analysis():

    data = request.json

    result = analyze_github(data['username'])

    return jsonify(result)