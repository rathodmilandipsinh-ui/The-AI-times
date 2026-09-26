import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import current_app,render_template


def send_registration_otp_email(user_email,otp):
    return send_otp_email(
    user_email,
    otp,
    "Verify Your Email Address",
    "Welcome to The AI Times!\n\nThank you for creating an account."
)

def send_reset_password_otp_email(user_email,otp):
    return send_otp_email(
    user_email,
    otp,
    "Password Reset Verification Code",
    "You requested to reset your password."
)

def send_otp_email(receiver_email, otp, subject, purpose):

    sender_email = current_app.config["MAIL_EMAIL"]
    sender_password = current_app.config["MAIL_PASSWORD"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    body = f"""
Hello,

{purpose}

Your verification code is:

{otp}

This code will expire in 5 minutes.

If you did not request this action, please ignore this email.

Regards,
The AI Times Team
"""

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return True

    except Exception as e:
        print(e)
        return False

def send_news_email(username,recipient_email,news_list):

    html_content = render_template(
        "news_email.html",
        username=username,
        subject="Today's AI News",
        news_list=news_list
    )
    
    sender_email = current_app.config["MAIL_EMAIL"]
    sender_password = current_app.config["MAIL_PASSWORD"]

    # Create email

    msg = MIMEMultipart("alternative")

    msg["Subject"] = "Today's AI News"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Email body
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)


    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("News email sent successfully.")

    except Exception as e:
        print("Error sending email:", e)


