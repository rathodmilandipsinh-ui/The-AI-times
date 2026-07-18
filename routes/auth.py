from flask import (
    Blueprint, 
    render_template,
    request,session,
    url_for,redirect,
    flash)
from werkzeug.security import generate_password_hash

from database import db
from models.user import User
from services.auth_service import (
    login_user,logout_user)



auth = Blueprint("auth",__name__)

@auth.route("/auth/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":

        if request.form.get("password") != request.form.get("confirm_password"):
            flash("Password Didn't Match!","error")
            return redirect(url_for("auth.signup")) 
        
        session["signup"] = {
            "name":request.form.get("name"),
            "email":request.form.get("email"),
            "password":request.form.get("password"),
            "confirm_password":request.form.get("confirm_password"),
            "interest":request.form.getlist("interest")
        }

        i1 = request.form.getlist("interest")
        i1 = ",".join(i1)

        u1 = User(name=request.form.get("name"),
                  email=request.form.get("email"),
                  password=generate_password_hash(request.form.get("password")),
                  interests=i1)
        session.clear()
        db.session.add(u1)
        db.session.commit()
        
        return redirect(url_for("home"))
    return render_template("auth/signup.html")

@auth.route("/auth/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        response,msg =  login_user(email,password)
        if not response:
            flash(msg,"error")
            return redirect(url_for("auth.login"))
        flash(msg,"success")
        return redirect(url_for("home"))
    return render_template("auth/login.html")


@auth.route("/auth/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))