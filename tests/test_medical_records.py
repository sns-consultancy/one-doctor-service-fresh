import unittest
from unittest.mock import patch, MagicMock, mock_open
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


class MedicalRecordsApiTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch('src.api.medical_records.db', new=MagicMock())
        self.mock_db = patcher.start()
        self.addCleanup(patcher.stop)
        # Ensure service uses the patched db
        from src.api import medical_records as med_module
        med_module.service.db = self.mock_db
        self.app = create_app().test_client()
        self.headers = {"x-api-key": "test_api_key"}

    @classmethod
    def tearDownClass(cls):
        for p in patches:
            p.stop()

    def test_create_and_get_record(self):
        mock_collection = MagicMock()
        self.mock_db.collection.return_value = mock_collection
        mock_collection.add.return_value = ("id", None)

        data = {"user_id": "user1", "age": 5, "medication": "test med"}
        response = self.app.post('/api/medical-records', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        posted_entry = response.get_json()['data']
        self.assertEqual(posted_entry['category'], 'young')

        mock_query = MagicMock()
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = posted_entry
        mock_collection.where.return_value = mock_query
        mock_query.stream.return_value = [mock_doc]
        self.mock_db.collection.return_value = mock_collection

        response = self.app.get('/api/medical-records/user1', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['medication'], 'test med')

    def test_missing_api_key(self):
        response = self.app.post('/api/medical-records', json={"user_id": "u", "age": 1})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
