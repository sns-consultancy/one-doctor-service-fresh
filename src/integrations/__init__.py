"""Wearable device integrations."""

from .fitbit import FitbitClient
from .apple_watch import AppleWatchClient
from .google_fit import GoogleFitClient
from .base import WearableClient

__all__ = [
    "WearableClient",
    "FitbitClient",
    "AppleWatchClient",
    "GoogleFitClient",
]
