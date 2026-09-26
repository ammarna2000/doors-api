@app.get("/db-test")
def db_test():
    return {
        "database_url_exists": DATABASE_URL is not None
    }
