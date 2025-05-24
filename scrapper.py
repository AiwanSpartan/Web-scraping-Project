import requests
from bs4 import BeautifulSoup

def get_price(name):          
    page_scrape = requests.get(f"https://store.steampowered.com/search/?term={name}")
    soup = BeautifulSoup(page_scrape.text, "html.parser")

    first_game = soup.find("a", class_="search_result_row")
    if not first_game:
        return "Game not found"

    price_div = first_game.find("div", class_="discount_final_price")
    if not price_div:
        return "Price not found"

    price_text = price_div.text.strip()
    return price_text
