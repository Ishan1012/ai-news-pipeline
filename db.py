from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_article(article):
    collection.update_one(
        {"url": article["url"]},
        {"$set": article},
        upsert=True
    )

def find_article_by_url(url):
    return collection.find_one({"url": url}, {"_id": 0})

def get_summary_by_url(url):
    article = find_article_by_url(url)
    return article.get("summary") if article else None

def fetch_articles_paginated(skip: int = 0, limit: int = 10):
    cursor = (
        collection
        .find({}, {"_id": 0})
        .sort("_id", -1)
        .skip(skip)
        .limit(limit)
    )
    return list(cursor)

def count_articles():
    return collection.count_documents({})