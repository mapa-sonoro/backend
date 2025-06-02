from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import os

simple_auth_bp = Blueprint('simple_auth', __name__)

# Contraseña encriptada (ejemplo: hash de "admin123")
HASHED_PASSWORD = os.environ.get('ADMIN_PASSWORD_HASH', '32768:8:1$nbjlk8Tz9gr1qssr$4264eba5a1851b24eb265416ab4fdac982b706e349e5a0b7e6662b414de0d35830f7dd55fae549c375231d65b868526fd689bd79b44dc670db9ca04e93c7aaf0.')

@simple_auth_bp.route('/verify-password', methods=['POST'])
def verify_password():
    from flask import request, jsonify
    import bcrypt

    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        password = data.get('password')
        if not password:
            return jsonify({"error": "No se proporcionó contraseña"}), 400

        # Hash estático de la contraseña "admin123" (solo para ejemplo)
        stored_hash = b'32768:8:1$nbjlk8Tz9gr1qssr$4264eba5a1851b24eb265416ab4fdac982b706e349e5a0b7e6662b414de0d35830f7dd55fae549c375231d65b868526fd689bd79b44dc670db9ca04e93c7aaf0.'

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return jsonify({"access": True}), 200
        else:
            return jsonify({"access": False}), 200

    except Exception as e:
        print("Error en verify_password:", e)
        return jsonify({"error": "Error en el servidor"}), 500
