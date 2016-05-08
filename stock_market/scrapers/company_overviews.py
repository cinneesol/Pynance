"""
scrape_exchange_listings company overviews for NASDAQ, AMEX, and NYSE
"""
import requests
import csv
prefix = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0=&exchange="
suffix = "&render=download"
exchanges = ['nasdaq','nyse','amex']

def scrape_exchange_listings():
    companies = []
    for exchange in exchanges:
        url = prefix+str(exchange)+suffix
        exchange_text = requests.get(url).text.split('\r\n')
        contents = csv.DictReader(exchange_text)
        for company in contents:
            companies.append(company)
    return companies
