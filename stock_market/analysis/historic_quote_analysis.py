from scrape_historic_quotes import scrape_historic_quotes
import re
from datetime import date
from statistics import mean, pstdev

def analyze(symbol,lock):
    """returns a dict of statistics about the historic quotes for the symbol"""
    quotes = sorted(scrape_historic_quotes(symbol), key=lambda x: x['Date'], reverse=True)
    analysis= {}
    analysis['avg_day_high']= mean([x['High'] for x in quotes[:30]])
    analysis['avg_day_low'] = mean([x['Low'] for x in quotes[:30]])
    analysis['day_high_std_dev'] = pstdev([x['High'] for x in quotes[:30]])
    analysis['day_low_std_dev'] = pstdev([x['Low'] for x in quotes[:30]])
    analysis['avg_close'] = mean([x['Close'] for x in quotes[:30]])
    analysis['close_std_dev'] = pstdev([x['Close'] for x in quotes[:30]])
    print(analysis)
    
if __name__=='__main__':
    analyze("team", None)