import os
import json
import base64
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load .env from parent folder
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

if not firebase_admin._apps:
    if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
        encoded = os.environ['FIREBASE_CREDENTIALS_BASE64']
        decoded = base64.b64decode(encoded).decode('utf-8')
        cred_dict = json.loads(decoded)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    elif os.environ.get('FIRESTORE_SERVICE_ACCOUNT'):
        path = os.environ['FIRESTORE_SERVICE_ACCOUNT']
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("No Firebase credentials found. Please set FIREBASE_CREDENTIALS_BASE64 or FIRESTORE_SERVICE_ACCOUNT.")

db = firestore.client()

docs = db.collection('users').stream()

for doc in docs:
    print(f"Document ID: {doc.id}")
    print(doc.to_dict())
    print("------")
