import os, sys, logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from datetime import timedelta

# Load .env only for local dev
load_dotenv(verbose=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Creating Flask application")
    app = Flask(__name__)

    # JWT + CORS
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
    JWTManager(app)
    CORS(app)

    # Blueprints (make sure these modules import quickly)
    from src.api.health import health_bp
    from src.api.authentication import authentication_bp
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(authentication_bp, url_prefix="/api/auth")

    @app.get("/")
    def index():
        return jsonify({"ok": True, "service": "one-doctor-service"})

    @app.get("/api/users")
    def list_users():
        # Lazy import so Firebase inits only when first used
        from src.db import get_db
        db = get_db()
        docs = db.collection("users").stream()
        users = [dict(doc.to_dict() | {"id": doc.id}) for doc in docs]
        return jsonify(users)

    @app.post("/api/users")
    def create_user():
        from src.db import get_db
        db = get_db()
        data = request.get_json(force=True) or {}
        ref = db.collection("users").document()
        ref.set(data)
        return jsonify({"id": ref.id}), 201

    @app.errorhandler(Exception)
    def handle_any(e):
        code = getattr(e, "code", 500)
        logger.exception("Unhandled error")
        return jsonify({"error": str(e)}), code

    logger.info("Flask application created successfully")
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", "30")))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7")))
