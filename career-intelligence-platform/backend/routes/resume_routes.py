from flask import Blueprint, request, jsonify
import pdfplumber
import re

resume_bp = Blueprint('resume', __name__)

SKILLS = [
    'python',
    'sql',
    'machine learning',
    'react',
    'django',
    'flask',
    'power bi',
    'tableau'
]

@resume_bp.route('/upload_resume', methods=['POST'])
def upload_resume():

    file = request.files['file']

    text = ''

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    extracted_skills = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill in lower_text:
            extracted_skills.append(skill)

    ats_score = min(len(extracted_skills) * 10, 100)

    return jsonify({
        'skills': extracted_skills,
        'ats_score': ats_score,
        'resume_text': text
    })