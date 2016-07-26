import requests 


def historic_quotes(symbol, year):
    url = str.format('http://ichart.finance.yahoo.com/table.csv?s={0}&c={1}',symbol,year)
    data = requests.get(url).text
    print(data)
