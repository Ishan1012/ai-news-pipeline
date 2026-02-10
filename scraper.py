import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_articles(url, max_articles=5):
    res = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0 (NewsBot/1.0)"}
    )
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    articles = []

    for link in soup.select("a[href]"):
        title = link.get_text(strip=True)
        href = link.get("href")
        keywords = ["artificial-intelligence", "ai", "machine-learning", "deep-learning"]

        if not title or len(title) < 20:
            continue
        if href.startswith("#") or "javascript:" in href.lower():
            continue
        if href == url:
            continue
        if all(keyword not in href for keyword in keywords):
            continue

        article_url = urljoin(url, href)

        articles.append({
            "title": title[:120],
            "url": article_url
        })

    return articles[:max_articles]

def fetch_article_text(url):
    res = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs)

    return text[:600]  # token safety

def classify_domain(text):
    rules = {"ai", "artificial intelligence", "machine learning", "deep learning", "neural network", "transformer"}

    text = text.lower()
    for keyword in rules:
        if keyword in text:
            return "AI"

    return "Research"

