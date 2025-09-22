# db.py
import os, sys, json, base64, tempfile, logging
from typing import Optional

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------------------------------------------------------
# Env & Logging
# -----------------------------------------------------------------------------
load_dotenv()  # safe even if no .env present

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("firebase-init")

IS_TESTING = os.getenv("FLASK_ENV") == "testing"
IS_DEVLIKE = os.getenv("FLASK_ENV") in {"development", "debug"} or os.getenv("DEBUG") == "True"

# -----------------------------------------------------------------------------
# Credential Resolution (priority order)
# -----------------------------------------------------------------------------
def _resolve_credentials() -> credentials.Certificate:
    """
    Returns a firebase_admin.credentials.Certificate based on the first
    available source (highest priority first).

    Priority:
      1) FIREBASE_CREDENTIALS_JSON        -> raw JSON string
      2) FIREBASE_CREDENTIALS_BASE64      -> base64 of the JSON
      3) FIREBASE_CREDENTIALS / FIREBASE_CREDENTIALS_PATH / FIRESTORE_SERVICE_ACCOUNT / GOOGLE_APPLICATION_CREDENTIALS -> file path
    """
    # 1) JSON text in env
    raw_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if raw_json:
        logger.info("Using FIREBASE_CREDENTIALS_JSON")
        try:
            return credentials.Certificate(json.loads(raw_json))
        except Exception as e:
            logger.error(f"Invalid FIREBASE_CREDENTIALS_JSON: {e}")
            raise

    # 2) Base64-encoded JSON in env
    b64 = os.getenv("FIREBASE_CREDENTIALS_BASE64") or os.getenv("FIREBASE_CREDENTIALS_B64")
    if b64:
        logger.info("Using FIREBASE_CREDENTIALS_BASE64")
        try:
            decoded = base64.b64decode(b64)
            # firebase_admin can take a dict, but we'll write a temp file for clarity
            data = json.loads(decoded.decode("utf-8"))
            return credentials.Certificate(data)
        except Exception as e:
            logger.error(f"Invalid FIREBASE_CREDENTIALS_BASE64: {e}")
            raise

    # 3) File path variants
    path_candidates = [
        os.getenv("FIREBASE_CREDENTIALS"),
        os.getenv("FIREBASE_CREDENTIALS_PATH"),
        os.getenv("FIRESTORE_SERVICE_ACCOUNT"),
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "firebase_key.json",  # final fallback if you keep the file in repo
    ]
    for p in path_candidates:
        if p and os.path.exists(p):
            logger.info(f"Using Firebase credentials file: {p}")
            return credentials.Certificate(p)

    # None found
    raise FileNotFoundError(
        "Firebase credentials not provided. Supply one of:\n"
        "- FIREBASE_CREDENTIALS_JSON (raw JSON)\n"
        "- FIREBASE_CREDENTIALS_BASE64 (base64 JSON)\n"
        "- FIREBASE_CREDENTIALS / FIREBASE_CREDENTIALS_PATH / FIRESTORE_SERVICE_ACCOUNT / GOOGLE_APPLICATION_CREDENTIALS (file path)"
    )

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------
_db_client: Optional[firestore.Client] = None

def _init_firebase_if_needed():
    global _db_client

    # Testing: provide a mock so unit tests run without real Firebase
    if IS_TESTING:
        logger.info("FLASK_ENV=testing detected; using mock Firebase app & DB.")
        from unittest.mock import MagicMock
        if not firebase_admin._apps:
            firebase_admin._apps = {"[DEFAULT]": MagicMock()}
        _db_client = MagicMock()
        return

    try:
        if not firebase_admin._apps:
            cred = _resolve_credentials()
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully.")
        else:
            logger.debug("Firebase already initialized; reusing existing app.")

        # Create Firestore client
        _db_client = firestore.client()
        logger.info("Firestore client ready.")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        if IS_DEVLIKE:
            logger.warning("Dev/Debug environment detected; falling back to mock DB.")
            from unittest.mock import MagicMock
            if not firebase_admin._apps:
                firebase_admin._apps = {"[DEFAULT]": MagicMock()}
            _db_client = MagicMock()
        else:
            # In prod, bubble up
            raise

# Run init on import
_init_firebase_if_needed()

# -----------------------------------------------------------------------------
# Public helpers
# -----------------------------------------------------------------------------
def get_app():
    """Return the firebase_admin app (mock in tests/dev fallback)."""
    if not firebase_admin._apps:
        _init_firebase_if_needed()
    # Return the first (default) app object
    return list(firebase_admin._apps.values())[0]

def get_db():
    """Return a Firestore client (or mock in testing/dev fallback)."""
    global _db_client
    if _db_client is None:
        _init_firebase_if_needed()
    return _db_client
# 3) File path variants
path_candidates = [
    os.getenv("FIREBASE_CREDENTIALS"),
    os.getenv("FIREBASE_CREDENTIALS_PATH"),
    os.getenv("FIRESTORE_SERVICE_ACCOUNT"),
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    "/etc/secrets/firebase.json",   # <— add this line (Render Secret File)
    "firebase_key.json",            # local-only fallback
]
