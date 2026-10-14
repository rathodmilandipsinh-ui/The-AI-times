from flask import Blueprint, jsonify,session,flash
from utils.auth import login_required

from database import db
from models.article import Article
from models.user import User
from flask import current_app

saved_news = Blueprint("saved_news", __name__)

@saved_news.route("/save/<int:article_id>", methods=["POST"])
def save_article(article_id):

    user_id = session.get("user_id")

    # Check login status
    if not user_id:
        flash("Please log in to save articles.","errror")
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

    saved_articles = list(user.saved_articles or [])

    if article_id in saved_articles:
        return jsonify({
            "success": True,
            "message": "Article already saved.",
            "saved": True
        }), 200

    try:
        saved_articles.append(article_id)
        user.saved_articles = saved_articles

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Article saved successfully.",
            "saved": True
        }), 200

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Failed to save article")

        return jsonify({
            "success": False,
            "message": "Unable to save article."
        }), 500