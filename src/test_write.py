import firebase_admin
from firebase_admin import credentials, firestore, initialize_app


def write_test_doc():
    """Write a simple document to Firestore for manual testing."""
    if not firebase_admin._apps:
        cred = credentials.Certificate("../firebase_key.json")
        initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection('users').document('test_user')
    doc_ref.set({
        'name': 'Test User',
        'email': 'testuser@example.com'
    })
    print("✅ Test document written.")


if __name__ == "__main__":
    write_test_doc()


