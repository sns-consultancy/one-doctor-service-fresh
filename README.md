<<<<<<< HEAD
# One-Doctor-Service

A modular Flask backend API for securely storing and retrieving health data using Firebase Firestore.

---

## Features

- REST API for health data (POST and GET)
- API key authentication via environment variable
- Firebase Firestore integration
- CORS enabled
- Modular, production-ready structure
- Unit tests with mocking

---

## Project Structure

```
one-doctor-service/
├── app.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── auth.py
│   └── api/
│       ├── __init__.py
│       └── health.py
├── tests/
│   └── test_health.py
├── requirements.txt
├── .env
└── ServiceAccountKey.json
```

---

## Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [Firebase Service Account Key JSON](https://firebase.google.com/docs/admin/setup)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sns-consultancy/one-doctor-service
   cd one-doctor-service
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # Or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Firebase service account key**
   - Place your Firebase service account JSON file in the project root (e.g., `ServiceAccountKey.json`).

5. **Set up environment variables**
   - Create a `.env` file in the project root:
     ```
     HEALTH_API_KEY=your-secret-api-key
     FIRESTORE_SERVICE_ACCOUNT=ServiceAccountKey.json
     ```

---

## Running the Application

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`.

---

## API Endpoints

### POST `/api/health`

Store health data for a user.

- **Headers:** `x-api-key: your-secret-api-key`
- **Body (JSON):**
  ```json
  {
    "user_id": "user123",
    "heartbeat": 72,
    "temperature": 98.6,
    "blood_pressure": "120/80",
    "oxygen_level": 98,
    "last_updated": "2024-05-15T12:00:00Z"
  }
  ```

### GET `/api/health/<user_id>`

Retrieve health data for a user.

- **Headers:** `x-api-key: your-secret-api-key`

---

## Testing

Run all unit tests:

```bash
python -m unittest discover tests
```

Tests use mocking for Firestore and API key validation.

---

## Deployment

### Production (Waitress)

```bash
pip install waitress
waitress-serve --port=8000 app:create_app
```

### Heroku

1. Add a `Procfile`:
   ```
   web: waitress-serve --port=$PORT app:create_app
   ```
2. Add `waitress` to `requirements.txt`.
3. Set environment variables in Heroku dashboard or CLI.
4. If needed, store your Firebase key as a config var and write it to a file at runtime.

---

## Notes

- Make sure your Firebase project is set up and Firestore is enabled.
- Never commit your `.env` or service account key to public repositories.
- For frontend or Tailwind CSS, see the frontend repo (if applicable).

---

## License

sns-consultancy
=======
# one-doctor-service-fresh
One Doctor Python Backend
>>>>>>> 5b692e3df8f4c50b4ac35f0627bb0179abfc3e2c
