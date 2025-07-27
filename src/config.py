import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# API key for your health API
API_KEY = os.environ.get('HEALTH_API_KEY', 'test_api_key')

# For Firebase credentials, check if we're on Heroku (using base64) or local
if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
    # We're on Heroku, use the base64 encoded credentials
    encoded = os.environ.get('FIREBASE_CREDENTIALS_BASE64')
    decoded = base64.b64decode(encoded).decode('utf-8')
    FIREBASE_CONFIG = json.loads(decoded)
    # Set DB_KEY to None since we're using the decoded config directly
    DB_KEY = None
else:
    # Local development, use the file path
    FIREBASE_CONFIG = None
    DB_KEY = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')