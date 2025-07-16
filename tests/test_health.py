import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(dotenv_path='.env.test')

# Mock the file open operation
mock_file = mock_open(read_data='{"type": "service_account", "project_id": "test-project"}')

# Create patches before importing any app modules
patches = [
    patch('builtins.open', mock_file),  # This mocks the file open operation
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()),
    patch('firebase_admin.initialize_app', return_value=MagicMock()),
    patch('firebase_admin.firestore.client', return_value=MagicMock())
]

# Start all patches
for p in patches:
    p.start()

# Now it's safe to import app modules
from app import create_app

class HealthApiTestCase(unittest.TestCase):
    def setUp(self):
        # Patch Firestore db directly
        patcher = patch('src.api.health.db', new=MagicMock())
        self.mock_db = patcher.start()
        self.addCleanup(patcher.stop)
        self.app = create_app().test_client()
        self.headers = {"x-api-key": "test_api_key"}
        
    @classmethod
    def tearDownClass(cls):
        # Stop all patches
        for p in patches:
            p.stop()

    def test_health_post_success(self):
        # Mock Firestore set method
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document

        data = {
            "user_id": "testuser",
            "heartbeat": 70,
            "temperature": 98.6,
            "blood_pressure": "120/80",
            "oxygen_level": 98,
            "last_updated": "2024-05-25T12:00:00Z"
        }
        response = self.app.post('/api/health', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json()['status'])
        self.mock_db.collection.assert_called_with('health_data')
        mock_collection.document.assert_called_with('testuser')
        mock_document.set.assert_called_once()

    def test_health_get_success(self):
        # Mock Firestore get method
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document
        mock_document.get.return_value.exists = True
        mock_document.get.return_value.to_dict.return_value = {
            "heartbeat": 70,
            "temperature": 98.6,
            "blood_pressure": "120/80",
            "oxygen_level": 98,
            "last_updated": "2024-05-25T12:00:00Z"
        }

        response = self.app.get('/api/health/testuser', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json()['status'])
        self.assertEqual(response.get_json()['data']['heartbeat'], 70)
    
    def test_health_post_missing_api_key(self):
        data = {
            "user_id": "testuser",
            "heartbeat": 70,
            "temperature": 98.6,
            "blood_pressure": "120/80",
            "oxygen_level": 98,
            "last_updated": "2024-05-25T12:00:00Z"
        }
        # No headers sent
        response = self.app.post('/api/health', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized', response.get_json()['status'])

    def test_health_get_missing_api_key(self):
        response = self.app.get('/api/health/testuser')
        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized', response.get_json()['status'])

    def test_health_get_user_not_found(self):
        # Mock Firestore get method to simulate missing user
        mock_collection = MagicMock()
        mock_document = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_document
        mock_document.get.return_value.exists = False

        response = self.app.get('/api/health/nonexistentuser', headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json()['status'])
        self.assertIn('not found', response.get_json()['message'].lower())

    def test_health_post_missing_user_id(self):
        # Missing user_id in payload
        data = {
            "heartbeat": 70,
            "temperature": 98.6,
            "blood_pressure": "120/80",
            "oxygen_level": 98,
            "last_updated": "2024-05-25T12:00:00Z"
        }
        response = self.app.post('/api/health', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json()['status'])

if __name__ == '__main__':
    unittest.main()