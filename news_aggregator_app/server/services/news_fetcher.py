import requests
from server.config import Config
from server.services.categorizer import categorize_article
from server.repositories.article_repo import store_articles
from server.repositories.admin_repo import update_last_accessed_db
from server.services.notifier import send_batch_notifications

def fetch_news_from_newsapi():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={Config.NEWSAPI_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"[NewsAPI] Fetched {len(articles)} articles")
        update_last_accessed_db("News API")  # Update last_accessed for News API
        return articles
    except Exception as e:
        print(f"[NewsAPI] Error fetching articles: {e}")
        return []

def fetch_news_from_thenewsapi():
    url = f"https://api.thenewsapi.com/v1/news/top?api_token={Config.THENEWSAPI_KEY}&locale=us"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("data", [])
        print(f"[TheNewsAPI] Fetched {len(articles)} articles")
        update_last_accessed_db("The News API")  # Update last_accessed for The News API
        return articles
    except Exception as e:
        print(f"[TheNewsAPI] Error fetching articles: {e}")
        return []

def fetch_and_store_news():
    articles = []
    for fetcher in [fetch_news_from_newsapi, fetch_news_from_thenewsapi]:
        for item in fetcher():
            category = item.get("category") or categorize_article(
                (item.get("title") or "") + " " + (item.get("description") or "")
            )
            articles.append({
                "title": item.get("title"),
                "content": item.get("description"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("name", "Unknown") if isinstance(item.get("source"), dict) else item.get("source", "Unknown"),
                "category": category,
                "published_at": item.get("publishedAt") or item.get("published_at")
            })
    print(f"[Fetcher] Total articles to store: {len(articles)}")
    store_articles(articles)
    send_batch_notifications()