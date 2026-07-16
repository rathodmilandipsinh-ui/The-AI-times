from flask import Flask,render_template
import os 

from config import Config
from database import db
from routes.auth import auth


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

app.register_blueprint(auth)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # app.run(
    #     host="0.0.0.0",
    #     port=int(os.environ.get("PORT", 5000)),
    #     debug=True
    # )

    app.run(debug=True)