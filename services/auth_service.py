from flask import session

from database import db
from models.user import User
from services.otp_service import generate_otp 
from services.email_service import send_otp_email
from services.password_service import (
    hash_password,
    verify_password
)
from services.otp_service import (
    generate_otp,
    can_resend,
    resend_remaining
)


def register_user(fullname, email, password):

    user = User.query.filter_by(email=email).first()

    if user:
        return False, "Email already exists."

    otp = generate_otp()

    session["signup_data"] = {
        "fullname": fullname,
        "email": email,
        "password": hash_password(password)
    }

    session["otp_purpose"] = "signup"

    if not send_otp_email(email, otp):
        return False, "Unable to send verification email."

    return True, "Verification code sent successfully."


def login_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        return False, "Invalid email or password."

    if not verify_password(user.password, password):
        return False, "Invalid email or password."

    session["user_id"] = user.id

    return True, "Login successful."


def logout_user():

    session.clear()

def forgot_password(email): 
    user = User.query.filter_by(email=email).first() 

    if not user: 
        return False, "No account found with this email." 
    
    otp = generate_otp() 
    session["reset_email"] = email 
    session["otp"] = otp

    if not send_otp_email(email, otp): 
        return False, "Unable to send OTP email."
    
    return True, "Verification code sent successfully."

def reset_password(new_password):

    email = session.get("reset_email")

    if not email:
        return False, "Password reset session has expired."

    user = User.query.filter_by(email=email).first()

    if not user:
        return False, "User not found."

    user.password = hash_password(new_password)

    db.session.commit()

    session.pop("reset_email", None)

    return True, "Password reset successfully."


def create_user_from_session():

    signup_data = session.get("signup_data")

    if not signup_data:
        return False, "Signup session expired."

    new_user = User(
        fullname=signup_data["fullname"],
        email=signup_data["email"],
        password=signup_data["password"]
    )

    db.session.add(new_user)
    db.session.commit()

    session.pop("signup_data", None)
    session.pop("otp_purpose", None)

    return True, "Account created successfully."


def resend_otp():

    if not can_resend():
        return (
            False,
            f"Please wait {resend_remaining()} seconds before requesting another OTP."
        )

    purpose = session.get("otp_purpose")

    if purpose == "signup":

        signup_data = session.get("signup_data")

        if not signup_data:
            return False, "Signup session expired."

        email = signup_data["email"]

    elif purpose == "reset_password":

        email = session.get("reset_email")

        if not email:
            return False, "Password reset session expired."

    else:
        return False, "Invalid OTP request."

    otp = generate_otp()

    if not send_otp_email(email, otp):
        return False, "Unable to send OTP email."

    return True, "A new OTP has been sent successfully."

