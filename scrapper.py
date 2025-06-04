import requests
from bs4 import BeautifulSoup
import re

def get_price(name):
    headers = {"User-Agent": "Mozilla/5.0"}      
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

#uses API calling instead of HTML parsing, API calling is usually more reliable, use if possible 
def get_reg_price(gameID, region):
    page_scrape = requests.get(
        "https://store.steampowered.com/api/appdetails",
        params={"appids": gameID, "cc": region, "l": "en"},
    )
    data = page_scrape.json()

    app_data = data.get(gameID)
    if not app_data:
        return "Game not found"
    
    price_info = app_data["data"].get("price_overview")
    if not price_info:
        return "Price not found"
    
    return price_info.get("final_formatted")


def get_id(name):
    headers = {"User-Agent": "Mozilla/5.0"}      
    page_scrape = requests.get(f"https://store.steampowered.com/search/?term={name}", headers = headers)
    soup = BeautifulSoup(page_scrape.text, "html.parser")

    for a in soup.find_all('a', href = True):
        if "/app/" in a['href']:
            match = re.search(r'/app/(\d+)/', a['href'])
            if match:
                game_id = match.group(1)
                break
    return game_id