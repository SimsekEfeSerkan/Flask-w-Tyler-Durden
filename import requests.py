import requests
from bs4 import BeautifulSoup

def get_finviz_stock_data():
    url = "https://finviz.com/screener.ashx?v=111&f=sh_price_o10,sh_avgvol_o1000,ta_highlow52w_a"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Hisse isimlerini ve fiyatlarını çekme
    stock_data = []
    for row in soup.find_all('tr', class_='table-light'):
        cells = row.find_all('td')
        if len(cells) > 1:
            ticker = cells[1].text.strip()
            price = cells[10].text.strip()
            stock_data.append({"ticker": ticker, "price": price})

    return stock_data

# Veriyi çek ve yazdır
stocks = get_finviz_stock_data()
for stock in stocks:
    print(f"{stock['ticker']}: {stock['price']}")
