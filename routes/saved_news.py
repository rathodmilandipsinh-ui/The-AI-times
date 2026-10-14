from flask import Blueprint, jsonify,session,flash,redirect,url_for
from utils.auth import login_required

from database import db
from models.article import Article
from models.user import User
from flask import current_app

saved_news = Blueprint("saved_news", __name__)


@saved_news.route("/save/<int:article_id>", methods=["POST"])
def save_article(article_id):

    user_id = session.get("user_id")

    # Check login
    if not user_id:
        return jsonify({
            "success": False,
            "login_required": True,
            "message": "Please log in to save articles."
        }), 401

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({
            "success": False,
            "login_required": True,
            "message": "Your session is invalid. Please log in again."
        }), 401

    # Check article exists
    article = db.session.get(Article, article_id)

    if not article:
        return jsonify({
            "success": False,
            "message": "Article not found."
        }), 404

    # Read saved article IDs
    saved_articles = [
        int(saved_id)
        for saved_id in (user.saved_articles or [])
    ]

    try:
        if article_id in saved_articles:

            # Remove saved article
            saved_articles.remove(article_id)
            is_saved = False
            message = "Article removed from saved articles."

        else:

            # Save article
            saved_articles.append(article_id)
            is_saved = True
            message = "Article saved successfully."

        user.saved_articles = saved_articles
        db.session.commit()

        return jsonify({
            "success": True,
            "saved": is_saved,
            "message": message
        }), 200

    except Exception:
        db.session.rollback()

        current_app.logger.exception(
            "Failed to toggle saved article"
        )

        return jsonify({
            "success": False,
            "message": "Unable to update saved article."
        }), 500



@saved_news.route("/remove/<int:article_id>", methods=["POST"])
def remove_article(article_id):

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to manage saved articles.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(id=user_id).first()

    if not user:
        flash("User not found.", "error")
        return redirect(url_for("auth.login"))

    saved_articles = list(user.saved_articles or [])

    if article_id not in saved_articles:
        flash("Article is not in your saved articles.", "info")
        return redirect(url_for("user.saved_articles"))

    try:
        saved_articles.remove(article_id)
        user.saved_articles = saved_articles

        db.session.commit()

        flash("Article removed from saved articles.", "success")

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Failed to remove saved article")
        flash("Unable to remove article.", "error")

    return redirect(url_for("user.saved_articles"))