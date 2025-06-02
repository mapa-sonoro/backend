from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import os

simple_auth_bp = Blueprint('simple_auth', __name__)

# Contraseña encriptada (ejemplo: hash de "admin123")
HASHED_PASSWORD = os.environ.get('ADMIN_PASSWORD_HASH', '32768:8:1$nbjlk8Tz9gr1qssr$4264eba5a1851b24eb265416ab4fdac982b706e349e5a0b7e6662b414de0d35830f7dd55fae549c375231d65b868526fd689bd79b44dc670db9ca04e93c7aaf0.')

@simple_auth_bp.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.get_json()
    password = data.get('password')

    if password and check_password_hash(HASHED_PASSWORD, password):
        return jsonify({'access': True})
    return jsonify({'access': False}), 401
