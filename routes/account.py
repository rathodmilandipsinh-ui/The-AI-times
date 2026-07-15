from flask import Blueprint, render_template

account = Blueprint("account",__name__)

@account.route("/account/signup")
def signup():
    return render_template("account/signup.html")

@account.route("/account/login")
def login():
    return render_template("account/login.html")