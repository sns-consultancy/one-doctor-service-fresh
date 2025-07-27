"""Placeholder integration for Google Fit / Android health data."""
from .base import WearableClient


class GoogleFitClient(WearableClient):
    """Client for fetching data from Google Fit (not implemented)."""

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def fetch_vitals(self) -> dict:
        """Fetch health data from Google Fit. Raises NotImplementedError."""
        raise NotImplementedError("Google Fit integration not implemented")
