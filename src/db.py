import os
import sys
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
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
        if 'FIREBASE_CREDENTIALS_BASE64' in os.environ:
            logger.info("Found FIREBASE_CREDENTIALS_BASE64 environment variable")
            encoded = os.environ.get('FIREBASE_CREDENTIALS_BASE64')
            decoded = base64.b64decode(encoded).decode('utf-8')
            cred_dict = json.loads(decoded)
            cred = credentials.Certificate(cred_dict)
            logger.info("Successfully loaded Firebase credentials from base64")

        # Priority 2: FIREBASE_CREDENTIALS
        elif 'FIREBASE_CREDENTIALS' in os.environ:
            logger.info("Found FIREBASE_CREDENTIALS environment variable")
            cred_path = os.environ.get('FIREBASE_CREDENTIALS')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
            else:
                logger.error(f"Firebase credentials file not found: {cred_path}")
                raise FileNotFoundError(f"Firebase credentials file not found: {cred_path}")

        # Priority 3: FIRESTORE_SERVICE_ACCOUNT
        elif 'FIRESTORE_SERVICE_ACCOUNT' in os.environ:
            path = os.environ.get('FIRESTORE_SERVICE_ACCOUNT')
            logger.info(f"Using Firebase credentials file: {path}")
            if os.path.exists(path):
                cred = credentials.Certificate(path)
            else:
                logger.error(f"Firebase credentials file not found: {path}")
                raise FileNotFoundError(f"Firebase credentials file not found: {path}")

        # No credentials found
        else:
            logger.error("No Firebase credentials found in environment variables")
            raise ValueError("No Firebase credentials found")

        # Initialize Firebase
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        logger.info("Firebase initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        if os.environ.get('FLASK_ENV') in ('development', 'debug') or os.environ.get('DEBUG') == 'True':
            from unittest.mock import MagicMock

            if not firebase_admin._apps:
                firebase_admin._apps = {'[DEFAULT]': MagicMock()}

            db = MagicMock()
            logger.warning("Using mock database due to initialization failure")
        else:
            raise
