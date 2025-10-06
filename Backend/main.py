from fastapi import FastAPI
from pydantic import BaseModel
from config import MODE
from model import predict_ckd
from database import init_db, insert_data, get_latest_prediction
import random

app = FastAPI(title="Arm-Ailment Band API")
init_db()

class SensorData(BaseModel):
    ph: float
    conductivity: float
    ammonia: float

@app.post("/send_sensor_data")
def send_sensor_data(data: SensorData):
    prediction = predict_ckd(data.dict())
    insert_data(data.ph, data.conductivity, data.ammonia, prediction)
    return {"prediction": prediction}

@app.get("/latest_prediction")
def latest_prediction():
    pred = get_latest_prediction()
    return {"prediction": pred} if pred is not None else {"message": "No data yet"}

@app.get("/get_sensor_data")
def get_sensor_data():
    if MODE == "dummy":
        return {
            "ph": round(random.uniform(5.0, 8.0), 2),
            "conductivity": round(random.uniform(300, 1200), 2),
            "ammonia": round(random.uniform(0.1, 2.0), 2)
        }
    elif MODE == "esp32":
        # Replace with real ESP32 data fetching logic
        return {
            "ph": 6.9,
            "conductivity": 850.5,
            "ammonia": 0.8
        }
