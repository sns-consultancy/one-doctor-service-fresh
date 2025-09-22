import os, json, base64, threading
import firebase_admin
from firebase_admin import credentials, firestore

_lock = threading.Lock()
_client = None
_inited = False

def _load_cred():
    # 1) Explicit file path (Render secret file or GOOGLE_APPLICATION_CREDENTIALS)
    file_path = os.getenv("FIREBASE_CREDENTIALS_FILE") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if file_path and os.path.exists(file_path):
        return credentials.Certificate(file_path)

    # 2) Raw JSON in env
    raw_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if raw_json:
        return credentials.Certificate(json.loads(raw_json))

    # 3) Base64 JSON in env (accept both *_B64 and *_BASE64 names)
    b64 = os.getenv("FIREBASE_CREDENTIALS_B64") or os.getenv("FIREBASE_CREDENTIALS_BASE64")
    if b64:
        return credentials.Certificate(json.loads(base64.b64decode(b64).decode("utf-8")))

    raise FileNotFoundError(
        "Firebase creds not found. Set one of: "
        "FIREBASE_CREDENTIALS_FILE or GOOGLE_APPLICATION_CREDENTIALS, "
        "FIREBASE_CREDENTIALS_JSON, FIREBASE_CREDENTIALS_B64."
    )

def get_db():
    """Initialize Firebase once and return a Firestore client."""
    global _client, _inited
    if _client:
        return _client
    with _lock:
        if not _inited:
            cred = _load_cred()
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            _client = firestore.client()
            _inited = True
    return _client
