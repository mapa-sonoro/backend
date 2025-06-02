from flask import Flask
from flask_cors import CORS
from controllers.markers import markers_bp
from auth_simple import simple_auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(markers_bp)
app.register_blueprint(simple_auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
