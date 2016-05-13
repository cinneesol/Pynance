from historic_quote_analysis import analyze
from scrapers.investopedia import historic_quotes
import sys



if __name__=='__main__':
    symbol = input("Enter symbol: ")
    print(analyze(historic_quotes(symbol.lower())))
    sys.exit()