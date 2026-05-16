from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career.db'
app.config['JWT_SECRET_KEY'] = 'secret'

CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.ml_routes import ml_bp

app.register_blueprint(auth_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(ml_bp)

if __name__ == '__main__':
    app.run(debug=True)