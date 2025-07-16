from flask import Blueprint, request, jsonify
from src.db import db
from src.auth import require_api_key

import logging

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['POST'])
@require_api_key
def receive_health_data():
    data = request.json
    try:
        user_id = data['user_id']
        health_data = {
            'heartbeat': data.get('heartbeat', 0),
            'temperature': data.get('temperature', 0.0),
            'blood_pressure': data.get('blood_pressure', '0/0'),
            'oxygen_level': data.get('oxygen_level', 0.0),
            'last_updated': data.get('last_updated', '')
        }
        db.collection('health_data').document(user_id).set(health_data)
        return jsonify({'status': 'success', 'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@health_bp.route('/health/<user_id>', methods=['GET'])
@require_api_key
def get_health_data(user_id):
    try:
        doc_ref = db.collection('health_data').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            logging.info(f"Health data retrieved for user: {user_id}")
            return jsonify({'status': 'success', 'data': doc.to_dict()}), 200
        else:
            logging.warning(f"No health data found for user: {user_id}")
            return jsonify({'status': 'error', 'message': 'User data not found'}), 404
    except Exception as e:
        logging.exception("Failed to retrieve health data")
        return jsonify({'status': 'error', 'message': str(e)}), 500
@health_bp.route('/health/medical-history', methods=['POST'])
@require_api_key
def save_medical_history():
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'status': 'error', 'message': 'User ID is required'}), 400
            
        medical_history = {
            'conditions': data.get('conditions', []),
            'allergies': data.get('allergies', []),
            'medications': data.get('medications', []),
            'surgeries': data.get('surgeries', []),
            'family_history': data.get('family_history', {}),
            'last_updated': data.get('last_updated', '')
        }
        
        db.collection('medical_history').document(user_id).set(medical_history)
        logging.info(f"Medical history saved for user: {user_id}")
        return jsonify({'status': 'success', 'message': 'Medical history saved successfully'}), 201
    except Exception as e:
        logging.exception("Failed to save medical history")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@health_bp.route('/health/medical-history/<user_id>', methods=['GET'])
@require_api_key
def get_medical_history(user_id):
    try:
        doc_ref = db.collection('medical_history').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            logging.info(f"Medical history retrieved for user: {user_id}")
            return jsonify({'status': 'success', 'data': doc.to_dict()}), 200
        else:
            logging.warning(f"No medical history found for user: {user_id}")
            return jsonify({'status': 'error', 'message': 'Medical history not found'}), 404
    except Exception as e:
        logging.exception("Failed to retrieve medical history")
        return jsonify({'status': 'error', 'message': str(e)}), 500
