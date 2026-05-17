from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

users = []

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    user = {
        'email': data['email'],
        'password': generate_password_hash(data['password'])
    }

    users.append(user)

    return jsonify({'message': 'User Registered'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    for user in users:
        if user['email'] == data['email']:
            if check_password_hash(user['password'], data['password']):
                token = create_access_token(identity=user['email'])
                return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'})