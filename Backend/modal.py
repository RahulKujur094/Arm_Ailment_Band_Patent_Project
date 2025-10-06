import joblib
import numpy as np

MODEL_PATH = "model/catboost_model.cbm"
model = None

def load_model():
"""Lazy load CatBoost model."""
global model
if model is None:
from catboost import CatBoostClassifier
model = CatBoostClassifier()
model.load_model(MODEL_PATH)
return model

def predict_ckd(sensor_data: dict) -> float:
"""
sensor_data: dict with keys ['ph', 'conductivity', 'ammonia']
Returns prediction probability between 0 and 1
"""
mdl = load_model()
X = np.array([[sensor_data['ph'],
sensor_data['conductivity'],
sensor_data['ammonia']]])
prob = mdl.predict_proba(X)[0][1]
return float(prob)
