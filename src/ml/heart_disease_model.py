import math
from typing import Dict

# Simple logistic regression weights trained offline on the UCI Heart Disease dataset
FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol',
    'fbs', 'restecg', 'thalach', 'exang', 'oldpeak',
    'slope', 'ca', 'thal'
]

# Coefficients approximated from a logistic regression model
WEIGHTS = [
    0.02, -1.5, 1.2, 0.015, 0.005,
    0.6, 0.2, -0.03, 1.0, 0.8,
    0.5, 0.4, -0.8
]
INTERCEPT = -5.0

def predict_risk(features: Dict[str, float]) -> float:
    """Return the probability of heart disease."""
    z = INTERCEPT
    for name, weight in zip(FEATURES, WEIGHTS):
        value = float(features.get(name, 0))
        z += weight * value
    return 1 / (1 + math.exp(-z))

def predict_class(features: Dict[str, float], threshold: float = 0.5) -> int:
    """Return 1 if risk >= threshold else 0."""
    return int(predict_risk(features) >= threshold)
