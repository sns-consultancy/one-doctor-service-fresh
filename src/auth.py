import logging
from functools import wraps
from flask import request, jsonify
from src.config import API_KEY
from firebase_admin import firestore
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('x-api-key')
        if key != API_KEY:
            logging.warning("Unauthorized access attempt.")
            return jsonify({'status': 'unauthorized', 'message': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function