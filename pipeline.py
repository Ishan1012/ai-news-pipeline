from scraper import scrape_articles, fetch_article_text, classify_domain
from cleaner import clean_text
from llm_processor import process_article
from db import save_article
from config import SCRAPE_SOURCES

def run_pipeline():
    for source in SCRAPE_SOURCES:
        articles = scrape_articles(source)
        print(articles)

        for art in articles:
            clean = clean_text(art["title"])
            text = fetch_article_text(art["url"])

            print(text)

            domain = classify_domain(text)
            summary = process_article(text)

            save_article({
                "title": clean,
                "url": art["url"],
                "domain": domain,
                "summary": summary
            })

            print(summary)