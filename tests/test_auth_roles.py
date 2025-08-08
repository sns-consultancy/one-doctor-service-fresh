import unittest
from unittest.mock import patch, MagicMock, mock_open
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(dotenv_path='.env.test')

mock_file = mock_open(read_data='{"type": "service_account", "project_id": "test-project"}')

patches = [
    patch('builtins.open', mock_file),
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()),
    patch('firebase_admin.initialize_app', return_value=MagicMock()),
    patch('firebase_admin.firestore.client', return_value=MagicMock()),
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

    def test_signup_login_and_switch_role(self):
        users_collection = MagicMock()
        doc_ref = MagicMock()
        self.mock_db.collection.return_value = users_collection
        users_collection.document.return_value = doc_ref

        resp = self.app.post('/api/auth/signup', json={
            'username': 'doc1',
            'email': 'd@e.com',
            'password': 'pwd',
            'role': 'doctor'
        })
        self.assertEqual(resp.status_code, 201)
        doc_ref.set.assert_called_once()

        hashed = generate_password_hash('pwd')
        doc_ref.get.return_value.exists = True
        doc_ref.get.return_value.to_dict.return_value = {
            'username': 'doc1',
            'password': hashed,
            'role': 'doctor'
        }

        resp = self.app.post('/api/auth/login', json={'username': 'doc1', 'password': 'pwd'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['role'], 'doctor')

        resp = self.app.post('/api/auth/switch-role', json={'username': 'doc1', 'role': 'hospital'})
        self.assertEqual(resp.status_code, 200)
        doc_ref.update.assert_called_with({'role': 'hospital'})


if __name__ == '__main__':
    unittest.main()
