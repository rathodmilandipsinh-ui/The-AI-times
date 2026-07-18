
import random
from datetime import datetime, timedelta

from flask import session


OTP_EXPIRY_MINUTES = 5

RESEND_DELAY = 30


def generate_otp():

    otp = str(random.randint(100000, 999999))
    session["resend_after"] = (
        datetime.now() +
        timedelta(seconds=RESEND_DELAY)
    ).isoformat()
    session["otp"] = otp
    session["otp_expiry"] = (
        datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    ).isoformat()
    
    return otp


def verify_otp(user_otp):

    stored_otp = session.get("otp")
    expiry = session.get("otp_expiry")

    if not stored_otp or not expiry:
        return False, "OTP not found."

    if datetime.now() > datetime.fromisoformat(expiry):
        clear_otp()
        return False, "OTP has expired."

    if stored_otp != user_otp:
        return False, "Invalid OTP."

    clear_otp()

    return True, "OTP verified."


def clear_otp():

    session.pop("otp", None)
    session.pop("otp_expiry", None)


def get_otp_from_form(form):

    return (
        form.get("otp1", "") +
        form.get("otp2", "") +
        form.get("otp3", "") +
        form.get("otp4", "") +
        form.get("otp5", "") +
        form.get("otp6", "")
    )


def can_resend():

    resend_after = session.get("resend_after")

    if not resend_after:
        return True

    return datetime.now() >= datetime.fromisoformat(
        resend_after
    )

def resend_remaining():

    resend_after = session.get("resend_after")

    if not resend_after:
        return 0

    remaining = (
        datetime.fromisoformat(resend_after)
        - datetime.now()
    ).total_seconds()

    return max(0, int(remaining))