"""
scrape information from Yahoo Finance using YQL and 
various yahoo finance scrape pages
"""

from urllib.parse import quote,unquote
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

def floating_outstanding_shares(symbol):
    """returns the floating shares and outstanding shares of a stock"""
    url = """http://download.finance.yahoo.com/d/quotes.csv?s={0}&f=f6j2&e=.csv
""".format(symbol)
    data = requests.get(url)
    results = {'symbol':symbol,'float':"N/A",'outstanding':"N/A"}
    try:
        if data.status_code == 200:
            info = data.text.split(',')
            results['float']=int(info[0].strip())
            results['outstanding']=int(info[1].strip())
    except Exception as e:
        print(str(e)+"\t"+str(data.text))
    return results
        
    
def historic_data(symbol,endDate,startDate):
    """returns historic data for a stock in the given date range. 
    dates must be in ISO format NOTE: if no results come back, try 
    shortening the date range to be no more than 15 months due to a 
    constraint in YQL"""
    
    query = """
    SELECT * FROM yahoo.finance.historicaldata  WHERE symbol = '{0}'
    AND endDate='{1}' AND startDate='{2}'
    """.strip().replace("\n", "").format(symbol,endDate,startDate)
    print(query)
    request_url = prepare_query_url(query)
    print(request_url)
    return query_yql_json(request_url)

if __name__=='__main__':
    print(floating_outstanding_shares('cfr'))