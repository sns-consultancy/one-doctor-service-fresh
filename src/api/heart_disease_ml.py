from flask import Blueprint, request, jsonify
from src.auth import require_api_key
from src.ml.heart_disease_model import predict_risk, FEATURES

heart_ml_bp = Blueprint('heart_ml', __name__)

@heart_ml_bp.route('/heart-disease/predict', methods=['POST'])
@require_api_key
def predict_heart_disease():
    data = request.get_json() or {}
    risk = predict_risk(data)
    return jsonify({'status': 'success', 'risk': risk}), 200
