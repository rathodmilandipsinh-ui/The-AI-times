from flask import Blueprint,render_template,session

from models.user import User

user = Blueprint("user",__name__)


@user.route("/user/profile")
def profile():
    user = session.get("user_id")
    current_user = User.query.filter_by(id=user).first()
    return render_template("user/profile.html",current_user=current_user)