from fastapi import FastAPI
from db import collection

app = FastAPI()

@app.get("/news")
def get_news(limit: int = 10):
    return list(collection.find({}, {"_id": 0}).limit(limit))
