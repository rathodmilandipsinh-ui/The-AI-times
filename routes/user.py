from flask import Blueprint,render_template,session,redirect,url_for,request,flash

from models.user import User
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
        

    interests = get_interests()
    return render_template("user/profile.html",
                           current_user=current_user,
                           interests=interests,
                           user_interest_ids=user_interest_ids)


@user.route("/user/update-interests",methods=["POST"])
def update_user_route():
    response,msg = update_user(request.form)
    if not response:
        flash(msg,"error")
        return redirect(url_for("user.profile"))
    
    flash(msg,"success")
    return redirect(url_for("user.profile"))