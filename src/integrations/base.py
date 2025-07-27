class WearableClient:
    """Base class for wearable device integrations."""

    def fetch_vitals(self):
        """Return a dictionary of vital signs."""
        raise NotImplementedError
