from extensions import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    username = db.Column(db.String(30), unique=True)

    password = db.Column(db.String(255), nullable=False)

    interests = db.Column(db.Text)   # JSON or comma-separated list

    email_verified = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)