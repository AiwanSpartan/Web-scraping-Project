from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
import requests
from flask_restful import Api
from models import db, gameData
from scrapper import get_price, get_id, get_reg_price ,regional_to_euros, reg_code_converter
from resources import GameDataResource
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"
db.init_app(app)
api = Api(app)

load_dotenv("keys.env")

API_KEY = os.getenv("STEAM_API_KEY")

@app.route("/")
def home():
    return render_template("home.html")


def data_process():
    isMatching = False
    game_title = ""
    user_input = request.form.get("input") or None
    
    country = request.form.get("country") or None

    if not user_input or not country:
        return {
        "user_input": user_input,
        "country": country,
        "isMatching": isMatching,
        "game_title": None,
        "full_country": None,
        "user_reg_price": None,
        "user_reg_euros": None,
        "price_text": None
        }

    price_text, isMatching, game_title = get_price(user_input, isMatching, game_title)

    price_text = float(price_text.replace(",", ".").replace("€", "").strip())
    gameID = get_id(user_input)


    sel_reg = country
    user_reg_price = get_reg_price(gameID, sel_reg)
    user_reg_euros = regional_to_euros(sel_reg, user_reg_price)

    full_country = reg_code_converter(country)["country"] 

    #basiaclly removes all currency symbol for cleaner data
    # match = re.search(r"\d[\d,\.]*", user_reg_price)
    # user_reg_price = match.group().replace(",", "")

    game = gameData(
        name=user_input, 
        gameID=gameID, 
        euro_orig=price_text, 
        reg_price=user_reg_price, 
        reg_euro=user_reg_euros
        )
    db.session.add(game)
    db.session.commit()

    return {
        "user_input": user_input,
        "price_text": price_text,
        "isMatching": isMatching,
        "game_title": game_title,
        "full_country": full_country,
        "user_reg_price": user_reg_price,
        "user_reg_euros": user_reg_euros
    }


@app.route("/button", methods=["POST"])
def button_pressed():
    result = data_process()

    if result["user_input"] is None:
        return render_template("home.html", isInput = "")
    
    #html returns nothing so .get() is important here 
    if not result or not result.get("full_country"): 
        return render_template("home.html", isCountry = "")

    return render_template(
        "result.html", 
        isMatching = result["isMatching"],
        game = result["user_input"],
        gameTitle = result["game_title"],
        price = result["price_text"],
        region = result["full_country"],
        new_price = result["user_reg_price"],
        reg_euros = result["user_reg_euros"])

        
@app.route("/deal_search", methods=["GET", "POST"])
def get_deals():
    if request.method == "POST":
        submit = True
        result = data_process()
        if result["user_input"] is None:
            isEmpty = True
            return render_template("deals.html", isEmpty = isEmpty)
        
        return compare_all_regions(result["user_input"])
        # return render_template(
        #     "deals.html", 
        #     game = result["user_input"], 
        #     isMatching = result.get("isMatching"), 
        #     gameTitle = result.get("game_title"),
        #     submit = submit)
    
    return render_template("deals.html")


def compare_all_regions(user_input):
    REGIONS = ["AUD", "BRL", "CAD", "EUR", "INR", "JPY", "KRW", "MXN", "NZD", "SGD", "ZAR", "GBP", "USD"]

    isMatching = False
    game_title = ""
    price_text, isMatching, game_title = get_price(user_input, isMatching, game_title)
    price_text = float(price_text.replace(",", ".").replace("€", "").strip())
    gameID = get_id(game_title)

    prices = []
    for reg in REGIONS:
        try:
            reg_price = get_reg_price(gameID, reg)

            # Clean price string first (remove € and spaces)
            reg_price = reg_price.replace("€", "").replace(" ", "").replace("'", "").strip()
            
            # Only convert comma to dot for Brazil and Germany (EUR)
            if reg in ["BRL", "EUR"]:
                reg_price = reg_price.replace(",", ".")
                
            euro_price = regional_to_euros(reg, reg_price)
            full_name = reg_code_converter(reg)["country"]

            full_name = str(full_name).replace("'", "").strip()
            reg_price = str(reg_price).replace("'", "").strip()

            prices.append((full_name, reg_price, euro_price, reg))
        except Exception as e:
            print(f"Error with region {reg}: {e}")
            continue

    sorted_prices = sorted(prices, key=lambda x: x[2])  
    cheapest = sorted_prices[0] if sorted_prices else None

    submit = True

    return render_template("deals.html",
        user_input = user_input,
        isMatching = isMatching,
        gameTitle = game_title,
        gameID = gameID,
        orig_price = price_text,
        sorted_prices = sorted_prices,
        cheapest = cheapest,
        submit = submit
    )


@app.route("/hist", methods=["GET"])
def history():
    response = requests.get("http://localhost:5000/get_data")
    history = response.json()
    return render_template("history.html", history=history)


api.add_resource(GameDataResource, "/get_data")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)