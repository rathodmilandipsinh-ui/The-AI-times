from flask import Blueprint,render_template,session,redirect,url_for,request,flash

from models.user import User
from models.article import Article
from utils.auth import login_required
from data.data import get_interests
from services.user_service import update_user

user = Blueprint("user",__name__)

@user.route("/user/profile")
@login_required
def profile():
    user = session.get("user_id")
    current_user = User.query.filter_by(id=user).first()
    user_interest_ids = current_user.interests
    saved_articles = current_user.saved_articles

    latest_saved = Article.query.filter_by(id=saved_articles[-1]).first()
        

    interests = get_interests()
    return render_template("user/profile.html",
                           current_user=current_user,
                           interests=interests,
                           user_interest_ids=user_interest_ids,
                           saved_count=len(saved_articles), 
                           latest_saved=latest_saved)


@user.route("/user/update-interests",methods=["POST"])
def update_user_route():
    response,msg = update_user(request.form)
    if not response:
        flash(msg,"error")
        return redirect(url_for("user.profile"))
    
    flash(msg,"success")
    return redirect(url_for("user.profile"))

@user.route("/user/saved-articles")
def saved_articles():
    user = session.get("user_id")
    current_user = User.query.filter_by(id=user).first()
    saved_articles = current_user.saved_articles or []

    if user:

        articles = Article.query.filter(
            Article.id.in_(saved_articles)
        ).all()
    else:
        articles = []

    return render_template("user/saved-articles.html",articles=articles)