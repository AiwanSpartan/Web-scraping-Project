import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_restful import Api
from models import db, gameData
from scrapper import get_price, get_id, get_reg_price
from resources import GameDataResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"
db.init_app(app)
api = Api(app)

load_dotenv("keys.env")
API_KEY = os.getenv("STEAM_API_KEY")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/button", methods=["POST"])
def button_pressed():
    user_input = request.form.get("input")
    price_text = get_price(user_input)
    price_text = float(price_text.replace(",", ".").replace("€", "").strip())
    userID = get_id(user_input)
    user_reg_price = get_reg_price(user_input, aud)

    game = gameData(name=user_input, prices=price_text, gameID=userID)
    db.session.add(game)
    db.session.commit()

    return render_template("result.html", game=user_input, price=price_text, id=userID)

api.add_resource(GameDataResource, "/get_data")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
