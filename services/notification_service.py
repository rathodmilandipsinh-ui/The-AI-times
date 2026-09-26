from services.user_service import get_users
from services.email_service import send_news_email

def filter_news_for_user(user, news_list):
    """
    Filter articles based on the user's interests.

    Args:
        user: User model instance
        news_list: List of Article model instances

    Returns:
        List of articles matching the user's interests
    """

    if not user.interests:
        return []

    user_interests = set(user.interests)

    filtered_news = []

    for article in news_list:
        if not article.interest_ids:
            continue

        article_interests = set(article.interest_ids)

        # Check if at least one interest matches
        if user_interests & article_interests:
            filtered_news.append(article)

    return filtered_news

def get_personalized_news(users, news_list):

    result = {}

    for user in users:
        result[user.id] = filter_news_for_user(
            user,
            news_list
        )

    return result

def process_personalized_news(news_list):

    # Get verified users
    users = get_users()

    # Fetch new articles from NewsAPI
    if not news_list:
        print("No new articles fetched.")
        return

    # Match articles with user interests
    personalized_news = get_personalized_news(
        users,
        news_list
    )

    # Send emails
    for user in users:

        user_news = personalized_news.get(
            user.id,
            []
        )

        if not user_news:
            continue

        send_news_email(
            recipient_email=user.email,
            username=user.name,
            news_list=user_news
        )

        print(
            f"News email sent to {user.email} "
            f"({len(user_news)} articles)"
        )
