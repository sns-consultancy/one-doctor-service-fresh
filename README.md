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

## Role-based Authentication

The authentication API supports multiple user types so the backend can serve
patients, doctors and hospitals from a single service. Provide a `role` field
when signing up or logging in:

```bash
POST /api/auth/signup
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret",
  "role": "doctor"
}

POST /api/auth/login
{
  "username": "alice",
  "password": "secret",
  "role": "doctor"
}
```

Only users with matching credentials and role will be authenticated.

## Advanced Feature Roadmap

Planned enhancements for a comprehensive health platform include:

- Long-term health profiles with family linkage and developmental tracking.
- Detailed medical history, immunization records and document storage.
- Integration with wearable devices for vitals and early warning analytics.
- Diet, mental health and appointment scheduling modules.
- Secure emergency access and shareable reports for care providers.
