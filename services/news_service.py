import requests
from datetime import datetime
from flask import current_app

from database import db
from models.article import Article


# Maps each interest ID (from interests.json) to keywords we'll search for
# in the article title/description to tag it correctly
INTEREST_KEYWORDS = {
    1: ["artificial intelligence", " ai "],
    2: ["machine learning", " ml "],
    3: ["deep learning"],
    4: ["generative ai", "genai"],
    5: ["llm", "large language model", "gpt", "chatgpt"],
    6: ["nlp", "natural language processing"],
    7: ["computer vision"],
    8: ["ai agent", "autonomous agent"],
    9: ["robot", "robotics", "automation"],
    10: ["research", "study", "paper"],
    11: ["open source ai", "open-source ai"],
    12: ["ai ethics", "responsible ai"],
    13: ["ai startup", "startup"],
    14: ["healthcare ai", "medical ai"],
    15: ["education ai", "edtech"],
    16: ["business ai", "enterprise ai"],
    17: ["coding assistant", "copilot", "code generation"],
    18: ["ai tool", "ai app"],
    19: ["ai chip", "ai hardware", "gpu"],
    20: ["ai regulation", "ai policy", "ai law"],
}

def fetch_and_store_articles():
    from data.data import get_interests

    api_key = current_app.config.get("NEWSAPI_KEY")
    interests = get_interests()

    url = "https://newsapi.org/v2/everything"
    new_count = 0

    for interest in interests:
        params = {
            "q": f'"{interest["name"]}"',
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": api_key,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print(f"NewsAPI error for '{interest['name']}':", data.get("message"))
            continue

        for item in data.get("articles", []):
            article_url = item.get("url")
            if not article_url:
                continue

            existing = Article.query.filter_by(url=article_url).first()
            if existing:
                # article already exists — but it might match this interest too,
                # so add this interest_id if not already tagged
                if existing.interest_ids and interest["id"] not in existing.interest_ids:
                    existing.interest_ids = existing.interest_ids + [interest["id"]]
                continue

            title = item.get("title") or ""
            description = item.get("description") or ""

            published_at = None
            if item.get("publishedAt"):
                try:
                    published_at = datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    pass

            new_article = Article(
                title=title,
                description=description,
                url=article_url,
                image_url=item.get("urlToImage"),
                source=(item.get("source") or {}).get("name"),
                interest_ids=[interest["id"]],
                published_at=published_at,
            )
            db.session.add(new_article)
            new_count += 1

    db.session.commit()
    return new_count