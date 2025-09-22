# src/middleware/api_key.py
import os, hmac, logging
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request  # only used in the OR decorator

def _configured_keys():
    """
    Read keys from env:
      - INTERNAL_TOKEN (preferred)
      - or API_KEY
    Support comma-separated list for rotation: "key1,key2,key3"
    """
    raw = os.getenv("INTERNAL_TOKEN") or os.getenv("API_KEY") or ""
    return [k.strip() for k in raw.split(",") if k.strip()]

def _valid(key: str) -> bool:
    if not key:
        return False
    for k in _configured_keys():
        if hmac.compare_digest(key, k):  # constant-time compare
            return True
    return False

def require_api_key(view_func=None, header_name=None):
    """
    Decorator that requires a valid API key in the header.
    Default header: X-Internal-Token (falls back to X-API-Key).
    Usage:
        @require_api_key
        def handler(): ...
    or:
        @require_api_key(header_name="X-API-Key")
    """
    header = header_name or os.getenv("API_KEY_HEADER", "X-Internal-Token")

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            provided = request.headers.get(header) or request.headers.get("X-API-Key")
            if not _valid(provided):
                logging.warning("Unauthorized (API key) %s %s", request.method, request.path)
                return jsonify({"error": "unauthorized", "message": "Invalid or missing API key"}), 401
            return fn(*args, **kwargs)
        return wrapper

    return decorator if view_func is None else decorator(view_func)

def require_api_key_or_jwt(view_func=None, header_name=None):
    """
    Accept EITHER a valid API key OR a valid JWT.
    Useful for endpoints used by both services (internal) and browsers (JWT).
    """
    header = header_name or os.getenv("API_KEY_HEADER", "X-Internal-Token")

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            provided = request.headers.get(header) or request.headers.get("X-API-Key")
            if _valid(provided):
                return fn(*args, **kwargs)
            try:
                verify_jwt_in_request(optional=False)
                return fn(*args, **kwargs)
            except Exception:
                logging.warning("Unauthorized (no API key or JWT) %s %s", request.method, request.path)
                return jsonify({"error": "unauthorized"}), 401
        return wrapper
    return decorator if view_func is None else decorator(view_func)
