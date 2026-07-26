from database import db
from datetime import datetime
from sqlalchemy import JSON

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), unique=True, nullable=False)
    image_url = db.Column(db.String(500))
    source = db.Column(db.String(100))

    interest_ids = db.Column(JSON)   

    published_at = db.Column(db.DateTime)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)