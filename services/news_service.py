import requests
from datetime import datetime
from flask import current_app

from database import db
from models.article import Article


# AI categories used by interests.json
INTEREST_KEYWORDS = {
    1: [
        "artificial intelligence",
        "artificial-intelligence",
        " ai "
    ],
    2: [
        "machine learning",
        "machine-learning",
        " ml "
    ],
    3: [
        "deep learning",
        "neural network",
        "neural networks",
        "deep neural"
    ],
    4: [
        "generative ai",
        "generative artificial intelligence",
        "genai",
        "ai-generated",
        "ai generated"
    ],
    5: [
        "large language model",
        "large language models",
        "llm",
        "llms",
        "gpt",
        "chatgpt",
        "claude",
        "gemini"
    ],
    6: [
        "natural language processing",
        "nlp",
        "language model",
        "text analysis"
    ],
    7: [
        "robotics",
        "robot",
        "robots",
        "automation",
        "autonomous robot"
    ],
    8: [
        "ai research",
        "artificial intelligence research",
        "research paper",
        "ai paper",
        "arxiv"
    ],
    9: [
        "open source ai",
        "open-source ai",
        "open source artificial intelligence",
        "hugging face",
        "huggingface"
    ],
    10: [
        "coding assistant",
        "ai coding",
        "ai programmer",
        "github copilot",
        "copilot",
        "cursor ai",
        "code assistant"
    ]
}


# Queries used to find AI-related articles.
AI_QUERIES = [
    '"artificial intelligence"',
    '"generative AI"',
    '"machine learning"',
    '"deep learning"',
    '"large language model"',
    '"LLM"',
    '"GPT"',
    '"ChatGPT"',
    '"AI agents"',
    '"AI research"',
    '"AI model"',
    '"AI chip"',
    '"AI robotics"',
    '"AI coding assistant"'
]


# Terms that strongly indicate that AI is actually
# the main subject of an article.
STRONG_AI_TERMS = [
    "artificial intelligence",
    "artificial-intelligence",
    "generative ai",
    "machine learning",
    "deep learning",
    "large language model",
    "large language models",
    "llm",
    "llms",
    "gpt",
    "chatgpt",
    "gemini ai",
    "claude ai",
    "ai model",
    "ai models",
    "ai agent",
    "ai agents",
    "ai research",
    "ai-generated",
    "ai generated",
    "neural network",
    "neural networks",
    "natural language processing",
    "hugging face",
    "github copilot",
    "coding assistant"
]


def is_ai_relevant(title, description):
    """
    Determines whether AI is actually a meaningful part
    of the article instead of just being mentioned once.
    """

    text = f"{title or ''} {description or ''}".lower()

    # Strong AI terms
    strong_matches = 0

    for term in STRONG_AI_TERMS:
        if term in text:
            strong_matches += 1

    # If multiple strong AI concepts appear, keep it.
    if strong_matches >= 2:
        return True

    # A strong AI term in the TITLE is a very strong signal.
    title_text = (title or "").lower()

    for term in STRONG_AI_TERMS:
        if term in title_text:
            return True

    return False

def cleanup_non_ai_articles():
    """
    Remove articles already stored in the database
    that are not actually AI-related.
    """

    articles = Article.query.all()

    deleted_count = 0

    for article in articles:

        if not is_ai_relevant(
            article.title,
            article.description
        ):
            print(
                f"Deleting non-AI article: {article.title}"
            )

            db.session.delete(article)

            deleted_count += 1

    try:
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            f"Error cleaning articles: {e}"
        )

        raise

    print(
        f"Cleanup complete. Deleted {deleted_count} non-AI articles."
    )

    return deleted_count
    
def get_interest_ids(title, description):
    """
    Assign AI subcategories based on article content.
    """

    text = f"{title or ''} {description or ''}".lower()

    matched_interests = []

    for interest_id, keywords in INTEREST_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:
                matched_interests.append(interest_id)
                break

    return matched_interests


def fetch_and_store_articles():

    api_key = current_app.config.get("NEWSAPI_KEY")

    if not api_key:
        raise ValueError("NEWSAPI_KEY is not configured.")

    url = "https://newsapi.org/v2/everything"

    new_count = 0

    fetched_articles = []

    # Existing articles cache
    article_cache = {
        article.url: article
        for article in Article.query.all()
    }

    for query in AI_QUERIES:

        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 20,
            "apiKey": api_key,
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as e:

            print(
                f"NewsAPI request failed for '{query}': {e}"
            )

            continue

        if data.get("status") != "ok":

            print(
                f"NewsAPI error for '{query}': "
                f"{data.get('message')}"
            )

            continue

        for item in data.get("articles", []):

            article_url = item.get("url")

            if not article_url:
                continue

            title = item.get("title") or ""
            description = item.get("description") or ""

            # -----------------------------------------
            # AI RELEVANCE FILTER
            # -----------------------------------------

            if not is_ai_relevant(title, description):

                print(
                    f"Rejected non-AI article: {title}"
                )

                continue

            # -----------------------------------------
            # FIND AI SUBCATEGORIES
            # -----------------------------------------

            interest_ids = get_interest_ids(
                title,
                description
            )

            # If no AI category matched, reject it.
            if not interest_ids:

                print(
                    f"Rejected uncategorized AI article: {title}"
                )

                continue

            # -----------------------------------------
            # CHECK DUPLICATE
            # -----------------------------------------

            article = article_cache.get(article_url)

            if article:

                current_interests = (
                    article.interest_ids or []
                )

                updated = False

                for interest_id in interest_ids:

                    if interest_id not in current_interests:

                        current_interests.append(
                            interest_id
                        )

                        updated = True

                if updated:

                    article.interest_ids = current_interests

                fetched_articles.append(article)

                continue

            # -----------------------------------------
            # PARSE DATE
            # -----------------------------------------

            published_at = None

            if item.get("publishedAt"):

                try:

                    published_at = datetime.strptime(
                        item["publishedAt"],
                        "%Y-%m-%dT%H:%M:%SZ"
                    )

                except ValueError:

                    try:

                        published_at = datetime.fromisoformat(
                            item["publishedAt"].replace(
                                "Z",
                                "+00:00"
                            )
                        )

                    except ValueError:

                        published_at = None

            # -----------------------------------------
            # CREATE ARTICLE
            # -----------------------------------------

            new_article = Article(

                title=title,

                description=description,

                url=article_url,

                image_url=item.get("urlToImage"),

                source=(
                    item.get("source") or {}
                ).get("name"),

                interest_ids=interest_ids,

                published_at=published_at,
            )

            db.session.add(new_article)

            article_cache[article_url] = new_article

            fetched_articles.append(new_article)

            new_count += 1

    # -----------------------------------------
    # SAVE
    # -----------------------------------------

    try:

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            f"Error saving articles: {e}"
        )

        raise

    return new_count, fetched_articles