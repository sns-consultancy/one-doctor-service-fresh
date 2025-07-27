# One Doctor Service

This repository contains a Flask backend with sample APIs for health data. The project now includes utilities for reading vital signs from wearable devices.

## Wearable Integrations

New modules under `src/integrations` provide basic clients for different devices. Currently the Fitbit client includes a simple implementation using the public Fitbit API. Apple Watch and Google Fit clients are provided as placeholders for future expansion.

Example usage:

```python
from src.integrations import FitbitClient

client = FitbitClient(access_token="YOUR_TOKEN")
heart_data = client.fetch_vitals()
```

These helpers can be extended to parse additional vitals like heartbeat, pulse and body temperature.
