from flask import Flask, render_template, request
import os

from sqlalchemy import or_

from config import Config
from database import db
from routes.auth import auth
from routes.user import user
from routes.saved_news import saved_news
from models.article import Article
from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import fetch_and_store_articles
from datetime import datetime
from services.notification_service import process_personalized_news

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    from data.data import get_interests

    category = request.args.get("category", type=int)
    q = request.args.get("q", "").strip()

    query = Article.query

    # Search: filter in SQL by title/description
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Article.title.ilike(like),
                Article.description.ilike(like)
            )
        )

    articles = query.order_by(Article.published_at.desc()).all()

    # Category: interest_ids is a JSON list, so filter in Python
    if category:
        articles = [
            a for a in articles
            if a.interest_ids and category in [int(i) for i in a.interest_ids]
        ]

    articles = articles[:60]

    return render_template(
        "home.html",
        articles=articles,
        interests=get_interests(),
        selected_category=category,
        q=q
    )


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route('/about')
def about():
    return render_template('about.html')

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(saved_news)


def scheduled_fetch():
    with app.app_context():
        count, fetched_articles = fetch_and_store_articles()
        print(f"[Scheduler] Fetched {count} new articles.")
        process_personalized_news(fetched_articles)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduled_fetch,
        trigger="interval",
        hours=24,
        next_run_time=datetime.now()
    )
    scheduler.start()

    # app.run(
    #     host="0.0.0.0",
    #     port=int(os.environ.get("PORT", 5000)),
    #     debug=True
    # )

    app.run(debug=False)