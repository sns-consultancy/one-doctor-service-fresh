"""Integration utilities for Fitbit devices."""
import requests
from .base import WearableClient


class FitbitClient(WearableClient):
    """Client for accessing Fitbit health data."""

    API_URL = "https://api.fitbit.com"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def fetch_vitals(self) -> dict:
        """Fetch heart rate and other vitals from Fitbit API."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.API_URL}/1/user/-/activities/heart/date/today/1d.json"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
