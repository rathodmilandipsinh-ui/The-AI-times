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
    login_user,
    logout_user,
    forgot_password,
    reset_password,
    register_user,
    create_user_from_session,
    resend_otp)
from services.otp_service import (verify_otp,get_otp_from_form)



auth = Blueprint("auth",__name__)

@auth.route("/auth/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":

        if request.form.get("password") != request.form.get("confirm_password"):
            flash("Password Didn't Match!","error")
            return redirect(url_for("auth.signup")) 

        response,msg = register_user(request.form)

        if not response:
            flash(msg,"error")
            return redirect(url_for("auth.signup"))

        flash(msg,'success')
        return redirect(url_for("auth.otp_verification"))
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

@auth.route("/auth/forgot-password",methods=["GET","POST"])
def forgot_password_route():
    if request.method == "POST":
        email = request.form.get("email")
        response,msg = forgot_password(email)

        if not response:
            flash(msg,"error")
            return redirect(url_for("auth.forgot_password_route"))
        
        flash(msg,"success")
        return redirect(url_for("auth.otp_verification"))
    
    return render_template("auth/forgot-password.html")


@auth.route("/auth/otp-verification", methods=["GET", "POST"])
def otp_verification():
    if request.method == "POST":
        user_otp = get_otp_from_form(request.form)
        response,msg = verify_otp(user_otp)

        if not response:
            flash(msg,"error")
            return redirect(url_for("auth.otp_verification"))

        purpose = session["purpose"]
        flash(msg,"success")
        if purpose == "signup":
            create_user_from_session()
            return redirect(url_for("auth.login"))

        elif purpose == "reset-password":
            return redirect(url_for("auth.reset_password_route"))
    return render_template("auth/otp-verification.html")

@auth.route("/auth/reset-password",methods=["GET","POST"])
def reset_password_route():
    if request.method == "POST":
       response,msg =  reset_password(request.form.get("pw"))

       if not response:
           flash(msg,"error")
           return redirect(url_for("auth.reset_password_route"))
       
       flash(msg,"success")
       return redirect(url_for("auth.login"))
    
    return render_template("auth/reset-password.html")

@auth.route("/resend-otp",methods=["POST"])
def resend_otp_route():

    success, message = resend_otp()

    if success:
        flash(message, "success")
    else:
        flash(message, "error")

    return redirect(url_for("auth.otp_verification"))

@auth.route("/auth/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))