import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .models import db  # import shared db from models.py

# Load .env from project root (one level above the tarot_api/ package)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Create exactly ONE global SQLAlchemy() object that models import
# db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)

    # ----- DB URL (Postgres only, per your preference) -----
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required (Postgres).")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )

    # ----- CORS -----
    cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173")
    CORS(app, resources={r"*": {"origins": [cors_origin]}})

    # ----- DB init (bind the ONE db instance to THIS app) -----
    db.init_app(app)

    # ----- Routes -----
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # ----- Errors -----
    @app.errorhandler(404)
    def not_found(_err):
        return jsonify(error="Not Found"), 404

    @app.errorhandler(400)
    def bad_request(_err):
        return jsonify(error="Bad Request"), 400

    return app

# IMPORTANT:
# Do NOT create a global `app = create_app()` here.
# Use the factory via FLASK_APP=tarot_api.app:create_app (see commands below).
if __name__ == "__main__":
    # Running directly as a script (optional)
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)
