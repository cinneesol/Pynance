"""
scrape_exchange_listings company overviews for NASDAQ, AMEX, and NYSE
"""
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
def exchange_listings():
    """retrieves exchange listings for NYSE,AMEX, and NASDAQ markets
        from nasdaq.com
    """
    
    
    prefix = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0=&exchange="
    suffix = "&render=download"
    exchanges = ['nasdaq','nyse','amex']
    
    companies = []
    for exchange in exchanges:
        url = prefix+str(exchange)+suffix
        exchange_text = requests.get(url).text.split('\r\n')
        contents = csv.DictReader(exchange_text)
        for company in contents:
            companies.append(company)
    return companies

def summary_quote(symbol):
    """retrieves the summary quote from nadaq.com"""
    prefix = "http://www.nasdaq.com/symbol/"
    url = prefix+symbol.strip().lower()
    page = requests.get(url)
    soup=BeautifulSoup(page.text, 'lxml')
    outermost_table = soup.select("#quotes_content_left_InfoQuotesResults")[0]
    data_table = outermost_table.find("tbody")
    summary = {}
    for row in data_table.find_all("tr"):
        data_cells = row.find_all("td")
        key=data_cells[0].get_text().strip().split('\r\n')[0].replace('\xa0','')
        value = data_cells[1].get_text().strip().replace('\xa0','')
        summary[key]=value
    return summary

def option_chain(ticker, dateindex=0):
    """retrieves near term near money option chain for ticker 
      dateindex specifies how many months away from current month 
      to look for options.
    """
    prefix = "http://www.nasdaq.com/symbol/"
    suffix="/option-chain?dateindex="
    url = prefix+ticker.lower()+suffix+str(dateindex) 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    options_table = soup.select('#optionchain > div.OptionsChain-chart.borderAll.thin ')[0]\
    .find_all("table")[0]
    data_rows = options_table.find_all("tr")
    options = []
    for row in data_rows[1:]:
        data = row.find_all("td")
        call_option = {'symbol':ticker.upper(), 'type':'CALL'}
        call_option['date'] = datetime.strptime(data[0].get_text(), '%b %d, %Y')
        try:
            call_option['last_sale'] = float(data[1].get_text())
        except:
            call_option['last_sale'] = 0
        try:
            call_option['change'] = float(data[2].get_text())
        except:
            call_option['change'] = 0
        try:
            call_option['bid'] = float(data[3].get_text())
        except:
            call_option['bid'] = 0
        try:
            call_option['ask']= float(data[4].get_text())
        except:
            call_option['ask']= 0
        try:
            call_option['volume'] = float(data[5].get_text())
        except:
            call_option['volume'] = 0
        try:
            call_option['open_interest']= float(data[6].get_text())
        except:
            call_option['open_interest']=0
        try:
            call_option['strike']=float(data[8].get_text())
        except:
            call_option['strike']=0
            
        put_option = {'date': datetime.strptime(data[9].get_text(),'%b %d, %Y'),
                       'symbol':ticker.upper(),
                       'type':'PUT'
                      }
        try:
            put_option['last_sale'] = float(data[10].get_text())
        except:
            put_option['last_sale'] = 0
        try:
            put_option['change'] = float(data[11].get_text())
        except:
            put_option['change'] = 0
        try:
            put_option['bid'] = float(data[12].get_text())
        except:
            put_option['bid'] = 0
        try:
            put_option['ask']= float(data[13].get_text())
        except:
            put_option['ask']= 0
        try:
            put_option['volume'] = float(data[14].get_text())
        except:
            put_option['volume'] = 0
        try:
            put_option['open_interest']= float(data[15].get_text())
        except:
            put_option['open_interest']=0
        try:
            put_option['strike']=float(data[8].get_text())
        except:
            put_option['strike']=0
        options.append(call_option)
        options.append(put_option)
    return options
    
    
if __name__=='__main__':
    print(option_chain('amd', dateindex=3))