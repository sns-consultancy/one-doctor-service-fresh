# src/api/authentication.py
import os
from datetime import timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from firebase_admin import firestore as fa_fs

from src.db import get_db

authentication_bp = Blueprint("authentication", __name__)
USERS_COLL = os.getenv("FIRESTORE_USERS_COLLECTION", "users")

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def _get_user_by_email(db, email: str):
    return next(db.collection(USERS_COLL)
                .where("email", "==", email).limit(1).stream(), None)

def _get_user_by_username(db, username: str):
    return next(db.collection(USERS_COLL)
                .where("username", "==", username).limit(1).stream(), None)

@authentication_bp.post("/signup")
def signup():
    db = get_db()
    body = request.get_json(force=True) or {}

    username = _norm(body.get("username"))
    email = _norm(body.get("email"))
    password = body.get("password") or ""

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    if _get_user_by_email(db, email):
        return jsonify({"error": "Email already registered"}), 409
    if _get_user_by_username(db, username):
        return jsonify({"error": "Username already taken"}), 409

    pw_hash = generate_password_hash(password)

    doc_ref = db.collection(USERS_COLL).document()  # auto ID
    user_doc = {
        "username": username,
        "email": email,
        "passwordHash": pw_hash,
        "role": "user",
        "createdAt": fa_fs.SERVER_TIMESTAMP,
        "updatedAt": fa_fs.SERVER_TIMESTAMP,
    }
    doc_ref.set(user_doc)

    uid = doc_ref.id
    access = create_access_token(identity=uid, additional_claims={"email": email, "role": "user"})
    refresh = create_refresh_token(identity=uid)

    return jsonify({
        "id": uid,
        "email": email,
        "username": username,
        "role": "user",
        "access_token": access,
        "refresh_token": refresh
    }), 201

@authentication_bp.post("/login")
def login():
    db = get_db()
    body = request.get_json(force=True) or {}
    login_id = _norm(body.get("username") or body.get("email"))
    password = body.get("password") or ""

    if not login_id or not password:
        return jsonify({"error": "username/email and password are required"}), 400

    doc = _get_user_by_email(db, login_id) or _get_user_by_username(db, login_id)
    if not doc:
        return jsonify({"error": "invalid credentials"}), 401

    data = doc.to_dict()
    if not check_password_hash(data.get("passwordHash", ""), password):
        return jsonify({"error": "invalid credentials"}), 401

    uid = doc.id
    access = create_access_token(identity=uid, additional_claims={
        "email": data.get("email"),
        "role": data.get("role", "user")
    })
    refresh = create_refresh_token(identity=uid)

    return jsonify({
        "id": uid,
        "email": data.get("email"),
        "username": data.get("username"),
        "role": data.get("role", "user"),
        "access_token": access,
        "refresh_token": refresh
    })

@authentication_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = get_jwt_identity()
    new_access = create_access_token(identity=uid)
    return jsonify({"access_token": new_access})

@authentication_bp.get("/me")
@jwt_required()
def me():
    db = get_db()
    uid = get_jwt_identity()
    snap = db.collection(USERS_COLL).document(uid).get()
    if not snap.exists:
        return jsonify({"error": "user not found"}), 404
    data = snap.to_dict()
    return jsonify({
        "id": uid,
        "email": data.get("email"),
        "username": data.get("username"),
        "role": data.get("role", "user"),
        "createdAt": str(data.get("createdAt")),
        "updatedAt": str(data.get("updatedAt")),
    })
