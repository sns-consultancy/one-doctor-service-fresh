import os
import sys
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Check if we're in testing mode
is_testing = os.environ.get('FLASK_ENV') == 'testing'

if is_testing:
    logger.info("Test environment detected, using mock Firebase")
    from unittest.mock import MagicMock

    if not firebase_admin._apps:
        firebase_admin._apps = {'[DEFAULT]': MagicMock()}
    db = MagicMock()

else:
    try:
        cred = None

        # Priority 1: FIREBASE_CREDENTIALS_BASE64
        firebase_b64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
        if firebase_b64:
            logger.info("Found FIREBASE_CREDENTIALS_BASE64 environment variable")
            decoded_json = base64.b64decode(firebase_b64).decode("utf-8")
            cred_dict = json.loads(decoded_json)
            cred = credentials.Certificate(cred_dict)
            logger.info("Loaded Firebase credentials from base64")

        # Priority 2: FIREBASE_CREDENTIALS (path)
        elif "FIREBASE_CREDENTIALS" in os.environ:
            cred_path = os.environ.get("FIREBASE_CREDENTIALS")
            logger.info(f"Found FIREBASE_CREDENTIALS path: {cred_path}")
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
            else:
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

        # Priority 3: FIRESTORE_SERVICE_ACCOUNT (path)
        elif "FIRESTORE_SERVICE_ACCOUNT" in os.environ:
            cred_path = os.environ.get("FIRESTORE_SERVICE_ACCOUNT")
            logger.info(f"Found FIRESTORE_SERVICE_ACCOUNT path: {cred_path}")
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
            else:
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

        else:
            raise ValueError("No Firebase credentials found in environment variables")

        # Initialize Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        logger.info("Firebase initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")

        # Development fallback
        if os.environ.get('FLASK_ENV') in ('development', 'debug') or os.environ.get('DEBUG') == 'True':
            from unittest.mock import MagicMock

            if not firebase_admin._apps:
                firebase_admin._apps = {'[DEFAULT]': MagicMock()}

            db = MagicMock()
            logger.warning("Using mock Firestore client due to initialization failure")
        else:
            raise
