from flask import Blueprint,render_template,session

from models.user import User
from utils.auth import login_required
from data.data import get_interests

user = Blueprint("user",__name__)

@user.route("/user/profile")
@login_required
def profile():
    user = session.get("user_id")
    current_user = User.query.filter_by(id=user).first()

    user_interest_ids_temp = current_user.interests
    user_interest_ids = []
    for i in user_interest_ids_temp:
        user_interest_ids.append(int(i))
        

    interests = get_interests()
    print(user_interest_ids)
    return render_template("user/profile.html",current_user=current_user,interests=interests,user_interest_ids=user_interest_ids)