import sqlite3

DB_FILE = "sensor_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ph REAL,
                        conductivity REAL,
                        ammonia REAL,
                        prediction REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )''')
    conn.commit()
    conn.close()

def insert_data(ph, conductivity, ammonia, prediction):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO sensor_data (ph, conductivity, ammonia, prediction) VALUES (?, ?, ?, ?)",
                (ph, conductivity, ammonia, prediction))
    conn.commit()
    conn.close()

def get_latest_prediction():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT prediction FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
