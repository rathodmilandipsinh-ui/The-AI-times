import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

#     "SQLALCHEMY_DATABASE_URI" = (
#     os.environ.get("DB_URL")
#     or "sqlite:///users.db"
# )

    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    permanent_session_lifetime = timedelta(days=30)

    MAIL_EMAIL = os.environ.get("MAIL_EMAIL")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")