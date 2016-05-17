from historic_quote_analysis import analyze
from options_analysis import analyze_options
from scrapers.investopedia import historic_quotes,option_chain
import sys
import json


if __name__=='__main__':
    symbol = input("Enter symbol: ")
    analysis = analyze(historic_quotes(symbol.lower())) 
    analysis['last_quote']['Date']=analysis['last_quote']['Date'].isoformat()
    analysis['Date']= analysis['Date'].isoformat()
    analysis['option_chain_analysis']=analyze_options(option_chain(symbol.lower()))
    
    print(json.dumps(analysis))
    sys.exit()