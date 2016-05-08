"""
scrape_exchange_listings company overviews for NASDAQ, AMEX, and NYSE
"""
import requests
import csv
from bs4 import BeautifulSoup

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

if __name__=='__main__':
    print(summary_quote('cfr'))