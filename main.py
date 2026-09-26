from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

class Measurement(BaseModel):
    contract_number: str
    item_number: str
    width_1: int
    width_2: int
    width_3: int
    height_1: int
    height_2: int
    height_3: int

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

    return {"door_measurements_count": count}

@app.post("/measurement")
def create_measurement(data: Measurement):

    width_final = min(data.width_1, data.width_2, data.width_3)
    height_final = min(data.height_1, data.height_2, data.height_3)

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO door_measurements
        (
            contract_number,
            item_number,
            width_1,
            width_2,
            width_3,
            height_1,
            height_2,
            height_3,
            width_final,
            height_final
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        data.contract_number,
        data.item_number,
        data.width_1,
        data.width_2,
        data.width_3,
        data.height_1,
        data.height_2,
        data.height_3,
        width_final,
        height_final
    ))

    conn.commit()

    cur.close()
    conn.close()

    return {
        "status": "saved",
        "width_final": width_final,
        "height_final": height_final
    }
