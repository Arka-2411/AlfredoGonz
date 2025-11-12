from flask import Flask
import os
import time
import pymysql

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppassword")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_PORT = int(os.getenv("DB_PORT", 3306))

def connect_with_retry(retries=10, delay=3):
    for i in range(retries):
        try:
            conn = pymysql.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS,
                database=DB_NAME, port=DB_PORT, cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except Exception as e:
            print(f"DB connection failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after retries")

# Flask app
app = Flask(__name__)

# Ensure DB + table exist
def init_db():
    conn = connect_with_retry()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            conn.commit()

@app.route("/")
def hello():
    conn = connect_with_retry()
    with conn:
        with conn.cursor() as cur:
            # insert a visit
            cur.execute("INSERT INTO visits () VALUES ();")
            conn.commit()
            cur.execute("SELECT COUNT(*) AS cnt FROM visits;")
            row = cur.fetchone()
    return f"<h1>¡Hola mundo desde Flask + MySQL! 👋</h1><p>Visitas totales: {row['cnt']}</p>"
    
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
