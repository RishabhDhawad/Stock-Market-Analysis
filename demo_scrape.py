import requests
from bs4 import BeautifulSoup
# Scraping Price using Xpath with Beautifulsoup

def get_stock_info():
    url = "https://groww.in/stocks/ircon-international-ltd"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Attempt to find stock name (if available in static HTML)
    try:
        stock_name = soup.find("h1", class_="lpu38Head").text
    except Exception as e:
        stock_name = f"Error: {e}"

    # Attempt to find stock price (usually not present in static HTML)
    try:
    # Target the specific <span> inside a div with class 'lpu38Pri'
        price_wrapper = soup.find("div", class_="lpu38Pri")
        if price_wrapper:
            spans = price_wrapper.find_all("span")
            if len(spans) > 1:
                stock_price = spans[1].text.strip()
            else:
                stock_price = "Price span not found"
        else:
            stock_price = "Price wrapper not found"
    except Exception as e:
        stock_price = f"Error: {e}"

    return stock_name, stock_price

name, price = get_stock_info()
print("Stock Name:", name)
print("Stock Price:", price)
