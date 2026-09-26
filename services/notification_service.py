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