from flask import Flask, send_from_directory, session, redirect, url_for, render_template
from flask_cors import CORS
from controllers.markers import markers_bp
from auth_simple import simple_auth_bp
import os

app = Flask(__name__, static_folder='static')  # 👈 esta sí, pero es la ÚNICA línea
CORS(app)

app.secret_key = os.environ.get("SECRET_KEY", "clave-super-secreta-clave-super")


# registra los blueprints
app.register_blueprint(markers_bp)
app.register_blueprint(simple_auth_bp)

@app.route('/')
def serve_login():
    return send_from_directory('static', 'login.html')

@app.route('/login')
def serve_login_file():
    return send_from_directory('static', 'login.html')

# @app.route('/admin')
# def serve_admin_panel():
#     return send_from_directory('static', 'admin_panel.html')

@app.route('/admin')
def serve_admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('serve_login_file'))
    return render_template('admin_panel.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('serve_login_file'))


# importante: esto al final
if __name__ == '__main__':
    app.run(debug=True)
