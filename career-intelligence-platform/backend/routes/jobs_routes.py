from flask import Blueprint
from flask import request
from flask import jsonify

from utils.job_matcher import recommend_jobs

jobs_bp = Blueprint(
    'jobs',
    __name__
)

@jobs_bp.route(
    '/recommend',
    methods=['POST']
)
def recommend():

    data = request.json

    resume = data['resume']

    recommended_jobs = recommend_jobs(
        resume
    )

    return jsonify({
        'recommended_jobs':
        recommended_jobs
    })