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


def reg_price(gameID, region):
    headers = {"User-Agent": "Mozilla/5.0"}      
    page_scrape = requests.get(f"/2.0/get/app/{gameID}/{region}")
    soup = BeautifulSoup(page_scrape.text, "html.parser")

    first_game = soup.find("a", class_="search_result_row")
    if not first_game:
        return "Game not found"

    price_div = first_game.find("div", class_="discount_final_price")
    if not price_div:
        return "Price not found"

    reg_price = price_div.text.strip()
    return reg_price


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