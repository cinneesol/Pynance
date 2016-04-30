"""
scrape historic quote data from 
investopedia.com 

Dependencies: Requests, Lxml, BeautifulSoup 4
"""

import requests 
from bs4 import BeautifulSoup

def scrape_historic_quotes(ticker_symbol):
    quotes=[]
    url = "http://www.investopedia.com/markets/stocks/"+str(ticker_symbol)+"/historical"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'lxml')
    data_table = soup.find_all("table", class_="table-data")[0]
    header_row = data_table.find_all("th")
    data_rows = data_table.find_all("tr")
    for historic_quote in data_rows:
        quote = {}
        for i in range(0, len(header_row)):
            key = header_row[i].get_text()
            val = None
            try: 
                val = historic_quote.find_all("td")[i].get_text()
            except:
                continue
            quote[str(key)]=str(val)
        quotes.append(quote)
    return quotes
