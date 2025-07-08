import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os


load_dotenv("keys.env")

def get_price(name, isMatching, game_title):
    headers = {"User-Agent": "Mozilla/5.0"}      
    page_scrape = requests.get(f"https://store.steampowered.com/search/?term={name}")
    soup = BeautifulSoup(page_scrape.text, "html.parser")

    first_game = soup.find("a", class_="search_result_row")
    if not first_game:
        return "Game not found"
    
    title_span = first_game.find("span", class_="title")
    game_title = title_span.text.strip()

    if game_title.lower() != name.lower():
        isMatching = False
    else:
        isMatching = True

    price_div = first_game.find("div", class_="discount_final_price")
    if not price_div:
        return "Price not found"

    price_text = price_div.text.strip()

    return price_text, isMatching, game_title


def reg_code_converter(region):
    mapping = {
        "USD": {"country": "United States", "code": "US"},
        "GBP": {"country": "United Kingdom", "code": "GB"},
        "CAD": {"country": "Canada", "code": "CA"},
        "AUD": {"country": "Australia", "code": "AU"},
        "JPY": {"country": "Japan", "code": "JP"},
        "BRL": {"country": "Brazil", "code": "BR"},
        "EUR": {"country": "Germany", "code": "DE"},
        "INR": {"country": "India", "code": "IN"},
        "MXN": {"country": "Mexico", "code": "MX"},
        "KRW": {"country": "South Korea", "code": "KR"},
        "NZD": {"country": "New Zealand", "code": "NZ"},
        "SGD": {"country": "Singapore", "code": "SG"},
        "ZAR": {"country": "South Africa", "code": "ZA"}
    }
    return mapping.get(region, {"country": "Unknown", "code": "N/A"})  # default fallback


#uses API calling instead of HTML parsing, API calling is usually more reliable, use if possible 
def get_reg_price(gameID, region):
    region = reg_code_converter(region)["code"] 

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



def regional_to_euros(region, reg_price):
    EURO_KEY = os.getenv("EURO_CONVERTER_KEY")
    url = f"https://v6.exchangerate-api.com/v6/2e25d7f40f95494597d1f5be/latest/{region}"
    response = requests.get(url)

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode error:", e)
        return None

    if "conversion_rates" not in data or "EUR" not in data["conversion_rates"]:
        print("Error: 'conversion_rates' or 'EUR' key missing in API response")
        return None

    # Extract number from reg_price string
    match = re.search(r"\d+[\.,]?\d*", reg_price)
    if not match:
        print("Could not parse price")
        return None

    # convert comma to dot and manually remove euro sign for Brazil and Germany
    if region in ["BRL", "EUR"]:
        cleaned_price = reg_price.replace("€", "").replace(",", ".").strip()
        price_number = float(cleaned_price)
    else:
        price_number = float(match.group().replace(",", ""))

    rate = data["conversion_rates"]["EUR"]
    
    formatted_euros = rate * price_number
    return round(formatted_euros, 2)



def get_id(name):
    headers = {"User-Agent": "Mozilla/5.0"}      
    page_scrape = requests.get(f"https://store.steampowered.com/search/?term={name}", headers = headers)
    soup = BeautifulSoup(page_scrape.text, "html.parser")
    game_id = None

    for a in soup.find_all('a', href = True):
        if "/app/" in a['href']:
            match = re.search(r'/app/(\d+)/', a['href'])
            if match:
                game_id = match.group(1)
                break
    return game_id