import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(verbose=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.api.health import health_bp
from src.api.authentication import authentication_bp
from src.db import db  # Firestore client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Creating Flask application")
    try:
        app = Flask(__name__)

        # JWT config
        app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
        jwt = JWTManager(app)

        # Enable CORS
        CORS(app)

        # Register blueprints
        app.register_blueprint(health_bp, url_prefix="/api")
        app.register_blueprint(authentication_bp, url_prefix="/api/auth")

        # Default home route
        @app.route("/")
        def index():
            return jsonify({"status": "success", "message": "One Doctor Service API"})

        # /api/health GET (example data)
        @app.route("/api/health", methods=["GET"])
        def get_health():
            return jsonify({"data": "Example health data"})

        # /api/users GET (list Firestore users)
        @app.route("/api/users", methods=["GET"])
        def get_users():
            users_ref = db.collection("users")
            docs = users_ref.stream()
            users = [doc.to_dict() for doc in docs]
            return jsonify(users)

        # /api/users POST (create Firestore user)
        @app.route("/api/users", methods=["POST"])
        def create_user():
            data = request.json
            new_user_ref = db.collection("users").document()
            new_user_ref.set(data)
            return jsonify({"message": "User created successfully."}), 201

        # Global error handler
        @app.errorhandler(500)
        def handle_500(e):
            logger.error(f"Internal server error: {str(e)}")
            return jsonify({"error": str(e)}), 500

        logger.info("Flask application created successfully")
        return app

    except Exception as e:
        logger.critical(f"Failed to create Flask application: {str(e)}")
        raise

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
