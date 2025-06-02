from flask import Flask, send_from_directory
from flask_cors import CORS
from controllers.markers import markers_bp
from auth_simple import simple_auth_bp
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(markers_bp)
app.register_blueprint(simple_auth_bp)

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_login():
    return send_from_directory('static', 'login.html')

@app.route('/admin_panel.html')
def serve_admin_panel():
    return send_from_directory('static', 'admin_panel.html')