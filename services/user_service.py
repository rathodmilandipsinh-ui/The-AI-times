from flask import session

from database import db
from models.user import User

def update_user(form):
    u1 = User.query.filter_by(id=session.get("user_id")).first()
    if not u1:
        return False,"Session expired."

    purpose = form.get("purpose")
    
    if purpose == "interests":
        interests = form.getlist("interests")
        user_interest_ids = []
        for i in interests:
            user_interest_ids.append(int(i))
        u1.interests = user_interest_ids
        msg = "Interests Updated"

    if purpose == "name":
        u1.name = form.get("name")
        msg = "Name changed."

    db.session.commit()
    return True,msg