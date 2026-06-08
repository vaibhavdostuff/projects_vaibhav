from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config.config import Config

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app)

jwt = JWTManager(app)

# --------------------
# Register Blueprints
# --------------------

from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.ml_routes import ml_bp
from routes.jobs_routes import jobs_bp

app.register_blueprint(
    auth_bp,
    url_prefix='/api/auth'
)

app.register_blueprint(
    resume_bp,
    url_prefix='/api/resume'
)

app.register_blueprint(
    ml_bp,
    url_prefix='/api/ml'
)

app.register_blueprint(
    jobs_bp,
    url_prefix='/api/jobs'
)

# --------------------
# Create Database
# --------------------

with app.app_context():
    db.create_all()

@app.route('/')

def home():

    return {
        'status': 'running',
        'project': 'Career Intelligence Platform'
    }