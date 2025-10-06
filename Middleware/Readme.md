# Arm-Ailment Band – FastAPI Backend Interface

## Overview
This FastAPI backend powers the Arm-Ailment Band system.  
It provides REST API endpoints for:
- Receiving sensor data from the frontend or ESP32
- Running CKD risk predictions using the trained ML model
- Serving stored predictions and latest sensor readings

The frontend communicates with this backend entirely via HTTP requests.

---

## API Endpoints

## 1. **POST** `/send_sensor_data`
**Purpose:** Receives sensor readings (pH, conductivity, ammonia), stores them in the database, and runs a CKD risk prediction.

#### **Request Body (JSON):**
```json
{
  "ph": 6.9,
  "conductivity": 850.5,
  "ammonia": 0.8
}
```
Response (JSON):

```json

{
  "prediction": 0.82
}
```
#### Backend Handling:

main.py → send_sensor_data()

Calls predict_ckd() in model.py

Calls insert_data() in database.py


###  2. **GET /latest_prediction**
Purpose: Returns the most recent CKD risk prediction stored in the database.

Response (JSON):

```json

{
  "prediction": 0.82
}
```

#### Backend Handling:

main.py → latest_prediction()

Calls get_latest_prediction() in database.py


### 3. **GET /get_sensor_data**
Purpose: Returns the latest sensor readings from either:

Dummy Mode (simulated random values)

ESP32 Mode (real hardware readings)

#### Response (JSON) Example – Dummy Mode:

```json

{
  "ph": 6.8,
  "conductivity": 900.2,
  "ammonia": 0.7
}
```
#### Backend Handling:

main.py → get_sensor_data()

Mode determined by MODE in config.py

## Data Flow

1. **Frontend Request (Flutter)**

Uses http package to send GET/POST requests to backend.

Example:
```
dart

final res = await http.get(Uri.parse('$backendBaseUrl/latest_prediction'));
```

2. **Backend Processing (FastAPI)**

Receives request via main.py

Uses database.py for storage/retrieval

Uses model.py for predictions

3. **Backend Response (JSON)**

Returns JSON payload to the frontend

Flutter parses the JSON and updates the UI

## How to Run Backend Locally

```

bash

cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will run on:

```
cpp

http://127.0.0.1:8000
```

## Tech Stack
FastAPI – API framework

SQLite – Data storage

CatBoost – ML model

Pydantic – Request validation

Random module – Dummy Mode simulation
