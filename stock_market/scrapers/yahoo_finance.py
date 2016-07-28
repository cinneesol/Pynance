"""
scrape information from Yahoo Finance using YQL
"""

from urllib.parse import quote
import json
import requests 


def prepare_query_url(query):
    """given an unformatted or formatted  YQL query, return the GET rest url 
    to retrieve json data from YQL """
    url = """
    https://query.yahooapis.com/v1/public/yql?q={0}&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys
    """.strip()
    return url.format(quote(query))

def query_yql_json(request_url):
    """makes a GET request to the request url and returns the json data as a dict"""
    data = requests.get(request_url)
    if data.status_code == 200:
        return json.loads(data.text)
    else:
        raise Exception("Status code from yahoo YQL: {0}".format(data.status_code))
    
def historic_quotes(symbol, year):
    url = str.format('http://ichart.finance.yahoo.com/table.csv?s={0}&c={1}',symbol,year)
    data = requests.get(url).text
    print(data)


def dividend_history(symbol,startDate,endDate):
    query = """SELECT * FROM yahoo.finance.dividendhistory WHERE symbol='{0}'
     and endDate='{1}' AND startDate='{2}'""".format(symbol,endDate,startDate)
     
    request_url = prepare_query_url(query)
    return query_yql_json(request_url)

def quotes(symbol):
    """returns a quote for the given stock ticker from YQL"""
    query = """
    SELECT * 
    FROM yahoo.finance.quotes
    WHERE symbol='{0}'""".format(symbol)
    request_url = prepare_query_url(query)
    return query_yql_json(request_url)

if __name__=='__main__':
    print(quotes('CFR'))