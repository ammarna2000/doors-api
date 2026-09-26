from fastapi import FastAPI
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def home():
    return {"status": "working"}

@app.get("/db-test")
def db_test():
    return {
        "database_url_exists": DATABASE_URL is not None
    }
