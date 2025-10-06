# Arm-Ailment Band – Backend

This is the **FastAPI backend** for the Arm-Ailment Band project.  
It receives sensor data (pH, conductivity, ammonia) from either an **ESP32 device** or dummy test data, predicts the **Chronic Kidney Disease (CKD) probability** using a **CatBoost ML model**, and stores results in an SQLite database.

---

## Features
- **CatBoost ML Model** for CKD probability prediction (0–1 scale)
- **SQLite Database** to store historical sensor readings and predictions
- **FastAPI Endpoints** for sending and retrieving data
- **Two modes**:  
  - `"dummy"` → Generates random sensor values for local testing  
  - `"esp32"` → Fetches data from a real ESP32 device

---

## Folder Structure
```

backend/
│
├── main.py            # FastAPI API routes
├── model.py           # Loads CatBoost model & makes predictions
├── database.py        # SQLite DB operations
├── config.py          # MODE selection ("dummy" / "esp32")
├── requirements.txt   # Python dependencies
└── model/
└── catboost\_model.cbm  # Trained CatBoost model file

````

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd backend
    ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The backend can run in two modes:

* **Dummy mode** (random sensor data for testing)
* **ESP32 mode** (reads from actual ESP32 device)

Set the mode in **`config.py`**:

```python
# config.py
MODE = "dummy"  # or "esp32"
```

---

## Running the Server

```bash
uvicorn main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

---

## API Endpoints

### 1. Send Sensor Data (POST)

**`/send_sensor_data`**
Send pH, conductivity, and ammonia values to get a CKD prediction.

Example Request:

```bash
curl -X POST "http://127.0.0.1:8000/send_sensor_data" \
-H "Content-Type: application/json" \
-d '{"ph": 6.9, "conductivity": 850.5, "ammonia": 0.8}'
```

Example Response:

```json
{"prediction": 0.72}
```

---

### 2. Get Latest Prediction (GET)

**`/latest_prediction`**

Example:

```bash
curl "http://127.0.0.1:8000/latest_prediction"
```

Response:

```json
{"prediction": 0.72}
```

---

### 3. Get Sensor Data (GET)

**`/get_sensor_data`**

* In `"dummy"` mode → Returns random values.
* In `"esp32"` mode → Returns ESP32 readings.

Example Response:

```json
{
  "ph": 6.9,
  "conductivity": 850.5,
  "ammonia": 0.8
}
```

---

## Database

* SQLite database file: **`sensor_data.db`**
* Created automatically on first run.
* Table schema:

```sql
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ph REAL,
    conductivity REAL,
    ammonia REAL,
    prediction REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```


