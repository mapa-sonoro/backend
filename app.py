from flask import Flask
from flask_cors import CORS
from controllers.markers import markers_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(markers_bp)

if __name__ == '__main__':
    app.run(debug=True)
