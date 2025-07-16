import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("../firebase_key.json")
    initialize_app(cred)

db = firestore.client()

# Write a test document
doc_ref = db.collection('users').document('test_user')
doc_ref.set({
    'name': 'Test User',
    'email': 'testuser@example.com'
})

print("✅ Test document written.")


