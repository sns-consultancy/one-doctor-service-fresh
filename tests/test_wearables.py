import unittest
from unittest.mock import patch, MagicMock

from src.integrations.fitbit import FitbitClient


class FitbitClientTestCase(unittest.TestCase):
    @patch('src.integrations.fitbit.requests.get')
    def test_fetch_vitals(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {'activities-heart': []}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        client = FitbitClient('dummy-token')
        data = client.fetch_vitals()

        self.assertEqual(data, {'activities-heart': []})
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
