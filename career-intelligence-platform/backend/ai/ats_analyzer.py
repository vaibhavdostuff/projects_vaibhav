SKILLS = [
    'python',
    'sql',
    'react',
    'django',
    'flask',
    'machine learning',
    'deep learning',
    'power bi',
    'tableau',
    'javascript',
    'typescript',
    'nodejs',
    'mongodb',
    'postgresql'
]

def analyze_resume(text):

    lower_text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in lower_text:
            found_skills.append(skill)

    score = min(len(found_skills) * 8, 100)

    recommendations = []

    if 'project' not in lower_text:
        recommendations.append(
            'Add Projects Section'
        )

    if 'experience' not in lower_text:
        recommendations.append(
            'Add Experience Section'
        )

    if 'education' not in lower_text:
        recommendations.append(
            'Add Education Section'
        )

    if len(found_skills) < 5:
        recommendations.append(
            'Add More Technical Skills'
        )

    return {
        'ats_score': score,
        'skills': found_skills,
        'recommendations': recommendations
    }