from flask import Flask,render_template,request
import os 

from config import Config
from database import db
from routes.auth import auth
from routes.user import user
from models.article import Article
from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import fetch_and_store_articles
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    from data.data import get_interests

    category = request.args.get("category", type=int)

    all_articles = Article.query.order_by(Article.published_at.desc()).all()

    if category:
        articles = [a for a in all_articles if a.interest_ids and category in a.interest_ids]
    else:
        articles = all_articles

    articles = articles[:60]

    return render_template(
        "home.html",
        articles=articles,
        interests=get_interests(),
        selected_category=category
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

@app.route('/admin/fetch-news')
def fetch_news():
    from services.news_service import fetch_and_store_articles
    count = fetch_and_store_articles()
    return f"Fetched {count} new articles."


app.register_blueprint(auth)
app.register_blueprint(user)


def scheduled_fetch():
    with app.app_context():
        count = fetch_and_store_articles()
        print(f"[Scheduler] Fetched {count} new articles.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_fetch, trigger="interval", hours=24, next_run_time=datetime.now())
    scheduler.start()

    # app.run(
    #     host="0.0.0.0",
    #     port=int(os.environ.get("PORT", 5000)),
    #     debug=True
    # )

    app.run(debug=False)