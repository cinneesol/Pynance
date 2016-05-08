"""
scrape historic quote data from 
investopedia.com 

Dependencies: Requests, Lxml, BeautifulSoup 4
"""

import requests 
from bs4 import BeautifulSoup
from datetime import date 
import re
def toDate(string):
    """converts a string from "mm/dd/yyyy" to a date object"""
    fields = re.split("/", string, 3)
    return date(int(fields[2]),int(fields[0]),int(fields[1]))

def isNum(num):
    try:
        float(num.replace(',',''))
        return True
    except ValueError:
        return False
    
def scrape(ticker_symbol):
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
            if isNum(val):
                quote[str(key)]=float(val.replace(',',''))
            elif key.lower()=="date":
                quote[str(key)]=toDate(val)
            else:
                quote[str(key)]=str(val)
            quote["Symbol"]=ticker_symbol.upper()
        if len(quote.keys())>1:
            quotes.append(quote)
    return quotes