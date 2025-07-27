import unittest
from unittest.mock import patch, MagicMock, mock_open
from dotenv import load_dotenv

# Load environment variables for tests
load_dotenv(dotenv_path='.env.test')

# Patches similar to other tests to avoid Firebase initialization
patches = [
    patch('builtins.open', mock_open(read_data='{}')),
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()),
    patch('firebase_admin.initialize_app', return_value=MagicMock()),
    patch('firebase_admin.firestore.client', return_value=MagicMock())
]
for p in patches:
    p.start()

from app import create_app

class HeartDiseaseMLTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.headers = {'x-api-key': 'test_api_key'}

    @classmethod
    def tearDownClass(cls):
        for p in patches:
            p.stop()

    def test_predict_endpoint(self):
        data = {
            'age': 63,
            'sex': 1,
            'cp': 3,
            'trestbps': 145,
            'chol': 233,
            'fbs': 1,
            'restecg': 0,
            'thalach': 150,
            'exang': 0,
            'oldpeak': 2.3,
            'slope': 0,
            'ca': 0,
            'thal': 1
        }
        response = self.app.post('/api/heart-disease/predict', json=data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn('risk', body)
        self.assertGreaterEqual(body['risk'], 0)
        self.assertLessEqual(body['risk'], 1)

if __name__ == '__main__':
    unittest.main()
