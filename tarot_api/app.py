import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from .models import db

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def create_app() -> Flask:
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is required (Postgres).")

    # Normalize to psycopg3
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgresql://") and "+psycopg" not in db_url and "+psycopg2" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )

    # Allow comma-separated origins: "http://localhost:5173,https://your-site.com"
    cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173")
    origins = [o.strip() for o in cors_origin.split(",") if o.strip()]
    CORS(app, resources={r"*": {"origins": origins}})

    db.init_app(app)

    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(_err):
        return jsonify(error="Not Found"), 404

    @app.errorhandler(400)
    def bad_request(_err):
        return jsonify(error="Bad Request"), 400

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=True)
