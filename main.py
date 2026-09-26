from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def home():
    return {"status": "working"}

@app.get("/db-test")
def db_test():

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM door_measurements")

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "door_measurements_count": count
    }
