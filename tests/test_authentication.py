import unittest
from unittest.mock import patch, MagicMock, mock_open, ANY
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load test environment variables
load_dotenv(dotenv_path='.env.test')

# Patches to avoid Firebase initialization
patches = [
    patch('builtins.open', mock_open(read_data='{}')),
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()),
    patch('firebase_admin.initialize_app', return_value=MagicMock()),
    patch('firebase_admin.firestore.client', return_value=MagicMock())
]
for p in patches:
    p.start()

from app import create_app

class AuthenticationApiTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch('src.api.authentication.db', new=MagicMock())
        self.mock_db = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = create_app().test_client()

    @classmethod
    def tearDownClass(cls):
        for p in patches:
            p.stop()

    def test_signup_with_role(self):
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document

        data = {
            'username': 'doc1',
            'email': 'doc@example.com',
            'password': 'pass',
            'role': 'doctor'
        }
        response = self.app.post('/api/auth/signup', json=data)
        self.assertEqual(response.status_code, 201)
        mock_document.set.assert_called_with({
            'username': 'doc1',
            'email': 'doc@example.com',
            'password': ANY,
            'role': 'doctor'
        })
        self.assertEqual(response.get_json()['role'], 'doctor')

    def test_login_role_mismatch(self):
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document
        hashed = generate_password_hash('pass')
        mock_document.get.return_value.exists = True
        mock_document.get.return_value.to_dict.return_value = {
            'username': 'pat1',
            'email': 'pat@example.com',
            'password': hashed,
            'role': 'patient'
        }

        data = {'username': 'pat1', 'password': 'pass', 'role': 'doctor'}
        response = self.app.post('/api/auth/login', json=data)
        self.assertEqual(response.status_code, 403)

    def test_login_success(self):
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document
        hashed = generate_password_hash('pass')
        mock_document.get.return_value.exists = True
        mock_document.get.return_value.to_dict.return_value = {
            'username': 'pat1',
            'email': 'pat@example.com',
            'password': hashed,
            'role': 'patient'
        }

        data = {'username': 'pat1', 'password': 'pass', 'role': 'patient'}
        response = self.app.post('/api/auth/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['role'], 'patient')

if __name__ == '__main__':
    unittest.main()
