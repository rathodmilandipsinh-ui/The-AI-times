from flask import Flask,render_template
import os 

from config import Config
from extensions import db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # app.run(
    #     host="0.0.0.0",
    #     port=int(os.environ.get("PORT", 5000)),
    #     debug=True
    # )

    app.run(debug=True)