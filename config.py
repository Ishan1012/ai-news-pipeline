import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "news_db"
COLLECTION_NAME = "articles"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

LLM_MODELS = ["tngtech/deepseek-r1t-chimera:free","tngtech/deepseek-r1t2-chimera:free","nvidia/nemotron-3-nano-30b-a3b:free","stepfun/step-3.5-flash:free"]

SCRAPE_SOURCES = [
    "https://indianexpress.com/section/technology/artificial-intelligence/",
    "https://www.bbc.com/news/topics/ce1qrvleleqt",
    "https://www.financialexpress.com/"
]