"""Placeholder integration for Apple Watch / iPhone Health data."""
from .base import WearableClient


class AppleWatchClient(WearableClient):
    """Client for fetching data from Apple HealthKit (not implemented)."""

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def fetch_vitals(self) -> dict:
        """Fetch health data from Apple HealthKit. Raises NotImplementedError."""
        raise NotImplementedError("Apple HealthKit integration not implemented")
