# One Doctor Service

This repository contains a Flask backend with sample APIs for health data. The project now includes utilities for reading vital signs from wearable devices.

## Project structure

The repository is split into separate areas for the Python backend and the JavaScript frontend:

* `src/` – all Python modules powering the Flask API
* `frontend/` – React/Node client code and build tooling

Keeping the frontend in its own directory prevents Heroku from treating the project as a Node application so the Python backend can run without additional configuration.

## Wearable Integrations

New modules under `src/integrations` provide basic clients for different devices. Currently the Fitbit client includes a simple implementation using the public Fitbit API. Apple Watch and Google Fit clients are provided as placeholders for future expansion.

Example usage:

```python
from src.integrations import FitbitClient

client = FitbitClient(access_token="YOUR_TOKEN")
heart_data = client.fetch_vitals()
```

These helpers can be extended to parse additional vitals like heartbeat, pulse and body temperature.

## Heroku deployment

1. Install the Heroku CLI and log in with `heroku login`.
2. Create an app configured for Python:

   ```bash
   heroku create my-one-doctor-app --buildpack heroku/python
   ```

3. Set required environment variables (for example `HEALTH_API_KEY` and `FIREBASE_CREDENTIALS_BASE64`):

   ```bash
   heroku config:set HEALTH_API_KEY=... FIREBASE_CREDENTIALS_BASE64=...
   ```

4. Deploy:

   ```bash
   git push heroku main
   ```

Heroku will install dependencies from `requirements.txt`, use `runtime.txt` to select the Python version, and start the web process defined in the `Procfile`.
