from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from src.db import db

authentication_bp = Blueprint("authentication", __name__)

@authentication_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Save user to Firestore
    user_ref = db.collection("users").document(username)
    user_ref.set({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User created successfully", "status": "success"}), 201


@authentication_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Retrieve user from Firestore
    user_ref = db.collection("users").document(username)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print("User not found:", username)
        return jsonify({"error": "User not found"}), 404

    user_data = user_doc.to_dict()
    stored_hashed_password = user_data.get("password")

    print("Login attempt for:", username)
    print("Stored hash:", stored_hashed_password)
    print("Password provided:", password)

    if not check_password_hash(stored_hashed_password, password):
        print("Password check failed")
        return jsonify({"error": "Invalid credentials"}), 401

    print("Password check passed")
    return jsonify({"message": "Login successful", "status": "success"}), 200
