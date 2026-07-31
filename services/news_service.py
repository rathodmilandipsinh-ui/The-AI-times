import requests
from datetime import datetime
from flask import current_app

from database import db
from models.article import Article


# Maps each interest ID (from interests.json) to keywords we'll search for
# in the article title/description to tag it correctly
INTEREST_KEYWORDS = {
    1: ["artificial intelligence", " ai ", "artificial-intelligence"],
    2: ["machine learning", " ml ", "machine-learning"],
    3: ["deep learning", "neural network", "transformer"],
    4: ["generative ai", "genai", "ai-generated"],
    5: ["llm", "gpt", "chatgpt"],
    6: ["nlp", "natural language processing", "text analysis"],
    7: ["robotics", "robot", "automation"],
    8: ["ai research", "research paper", "arxiv"],
    9: ["open source ai", "open-source ai", "hugging face"],
    10: ["coding assistant", "copilot", "cursor"]
}

INTEREST_QUERIES = {
    1: "AI OR artificial intelligence OR OpenAI",
    2: "machine learning OR ML OR supervised learning",
    3: "deep learning OR neural network OR transformer",
    4: "generative AI OR GenAI OR AI-generated",
    5: "LLM OR GPT OR ChatGPT",
    6: "NLP OR natural language processing OR text analysis",
    7: "robotics OR robot OR automation",
    8: "AI research OR research paper OR arXiv",
    9: "open source AI OR open-source AI OR Hugging Face",
    10: "coding assistant OR GitHub Copilot OR Cursor"
}

def fetch_and_store_articles():
    from data.data import get_interests

    api_key = current_app.config.get("NEWSAPI_KEY")
    interests = get_interests()

    url = "https://newsapi.org/v2/everything"
    new_count = 0

    # Cache all existing articles by URL
    article_cache = {
        article.url: article
        for article in Article.query.all()
    }

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
            print(f"NewsAPI error for '{interest['name']}': {data.get('message')}")
            continue

        for item in data.get("articles", []):
            article_url = item.get("url")

            if not article_url:
                continue

            # Check if article already exists (database or current session)
            article = article_cache.get(article_url)

            if article:
                current_interests = article.interest_ids or []

                if interest["id"] not in current_interests:
                    article.interest_ids = current_interests + [interest["id"]]

                continue

            # Parse published date
            published_at = None
            if item.get("publishedAt"):
                try:
                    published_at = datetime.strptime(
                        item["publishedAt"],
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                except ValueError:
                    pass

            # Create new article
            new_article = Article(
                title=item.get("title") or "",
                description=item.get("description") or "",
                url=article_url,
                image_url=item.get("urlToImage"),
                source=(item.get("source") or {}).get("name"),
                interest_ids=[interest["id"]],
                published_at=published_at,
            )

            db.session.add(new_article)

            # Add to cache immediately so duplicates in this run are detected
            article_cache[article_url] = new_article

            new_count += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error saving articles: {e}")
        raise

    return new_count