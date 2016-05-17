"""
scrape historic quote data from 
investopedia.com 

Dependencies: Requests, Lxml, BeautifulSoup 4
"""

import requests 
from bs4 import BeautifulSoup
from datetime import date 
import re
import json

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
    
def get_month_letter_map():
    ml_map = {
              'A':1,
              'B':2,
              'C':3,
              'D':4,
              'E':5,
              'F':6,
              'G':7,
              'H':8,
              'I':9,
              'J':10,
              'K':11,
              'L':12
              }
    return ml_map

def parse_option_symbol(option_symbol):
    month_letter_map = get_month_letter_map()
    group_matching=re.match("([a-zA-Z]+)([0-9]{4})([a-zA-Z])([0-9]+)",option_symbol)
    symbol = group_matching.group(1)
    year = group_matching.group(2)[0:2]
    day = group_matching.group(2)[2:]
    month = group_matching.group(3)
    strike_price = group_matching.group(4)
    result = {'symbol':symbol,'year':year,'day':day,'month':month,'strike_price':strike_price}
    return result   
    
def historic_quotes(ticker_symbol):
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

def option_chain(ticker_symbol):
    """This one has a direct public facing api call that will return a JSON object with
    call and put data """
    url = "http://www.investopedia.com/vcb_api/markets/optionslist/?symbol="+str(ticker_symbol)
    content = requests.post(url)
    response = json.loads(content.text)
    months = [x['month'] for x in response['monthList']]
    year = response['monthList'][0]['year']
    print(year)
    call_options = []
    put_options = []
    for month in months:
        monthurl = url+"&month="+str(month)+"&year="+str(year)
        content = requests.post(monthurl)
        response = json.loads(content.text)
        for option in response['callsList']:
            parsed_symbol = parse_option_symbol(option['symbol'])
            option['symbol']=parsed_symbol['symbol']
            option['month']=month 
            option['day']=parsed_symbol['day']
            call_options.append(option)
        for option in response['putsList']:
            parsed_symbol = parse_option_symbol(option['symbol'])
            option['symbol']=parsed_symbol['symbol']
            option['month']=month 
            option['day']=parsed_symbol['day']
            put_options.append(option)
    return {'calls':call_options, 'puts':put_options, 'date':date.today().isoformat()}

if __name__=='__main__':
    print(json.dumps(option_chain('cfr')))

    