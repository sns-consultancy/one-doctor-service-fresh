# src/api/health.py
from flask import Blueprint,jsonify
import logging

from src.db import get_db
from src.auth import require_api_key

db = get_db()

log = logging.getLogger(__name__)
health_bp = Blueprint("health", __name__)

# Simple health check (no API key required)
@health_bp.get("/health")
def health_status():
    return jsonify({"ok": True, "service": "one-doctor-service", "status": "healthy"}), 200


@health_bp.post("/health")
@require_api_key
def receive_health_data():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    health_data = {
        "heartbeat": payload.get("heartbeat", 0),
        "temperature": payload.get("temperature", 0.0),
        "blood_pressure": payload.get("blood_pressure", "0/0"),
        "oxygen_level": payload.get("oxygen_level", 0.0),
        "last_updated": payload.get("last_updated", ""),
    }

    try:
        db.collection("health_data").document(user_id).set(health_data, merge=True)
        return jsonify({"status": "success", "message": "Data stored"}), 200
    except Exception as e:
        log.exception("Failed to store health data for %s", user_id)
        return jsonify({"status": "error", "message": str(e)}), 500


@health_bp.get("/health/<user_id>")
@require_api_key
def get_health_data(user_id):
    try:
        doc = db.collection("health_data").document(user_id).get()
        if doc.exists:
            log.info("Health data retrieved for user %s", user_id)
            return jsonify({"status": "success", "data": doc.to_dict()}), 200
        log.warning("No health data found for user %s", user_id)
        return jsonify({"status": "error", "message": "User data not found"}), 404
    except Exception as e:
        log.exception("Failed to retrieve health data for %s", user_id)
        return jsonify({"status": "error", "message": str(e)}), 500


@health_bp.post("/health/medical-history")
@require_api_key
def save_medical_history():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "User ID is required"}), 400

    medical_history = {
        "conditions": payload.get("conditions", []),
        "allergies": payload.get("allergies", []),
        "medications": payload.get("medications", []),
        "surgeries": payload.get("surgeries", []),
        "family_history": payload.get("family_history", {}),
        "last_updated": payload.get("last_updated", ""),
    }

    try:
        ref = db.collection("medical_history").document(user_id)
        existed = ref.get().exists
        ref.set(medical_history, merge=True)
        code = 200 if existed else 201
        msg = "Medical history updated" if existed else "Medical history created"
        log.info("%s for user %s", msg, user_id)
        return jsonify({"status": "success", "message": msg}), code
    except Exception as e:
        log.exception("Failed to save medical history for %s", user_id)
        return jsonify({"status": "error", "message": str(e)}), 500


@health_bp.get("/health/medical-history/<user_id>")
@require_api_key
def get_medical_history(user_id):
    try:
        doc = db.collection("medical_history").document(user_id).get()
        if doc.exists:
            log.info("Medical history retrieved for %s", user_id)
            return jsonify({"status": "success", "data": doc.to_dict()}), 200
        log.warning("No medical history found for %s", user_id)
        return jsonify({"status": "error", "message": "Medical history not found"}), 404
    except Exception as e:
        log.exception("Failed to retrieve medical history for %s", user_id)
        return jsonify({"status": "error", "message": str(e)}), 500
