from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
import os
import bcrypt

simple_auth_bp = Blueprint('simple_auth', __name__)

stored_hash = b'$2b$12$zbq08OGuHEQe.mbmo.iknubfPLfjB0q/RSCX1hSIuDXJvPS.r0UZm'

@simple_auth_bp.route('/verify-password', methods=['POST'])
def _password():
    try:
        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({"error": "No se proporcionó contraseña"}), 400

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            session['logged_in'] = True
            return jsonify({"access": True}), 200
        else:
            return jsonify({"access": False}), 200

    except Exception as e:
        print("Error en verify_password:", e)
        return jsonify({"error": "Error en el servidor"}), 500
