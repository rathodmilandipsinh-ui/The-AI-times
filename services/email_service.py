import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app


def send_otp_email(receiver_email, otp):

    sender_email = current_app.config["MAIL_EMAIL"]
    sender_password = current_app.config["MAIL_PASSWORD"]

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Password Reset Verification Code"

    body = f"""
Hello,

Your password reset verification code is:

{otp}

This code will expire in 5 minutes.

If you didn't request a password reset, please ignore this email.

Regards,
The AI Times
"""

    message.attach(MIMEText(body, "plain"))

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()
            server.login(sender_email, sender_password)

            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )

        return True

    except Exception as e:

        print(e)

        return False

