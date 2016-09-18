
from datetime import datetime

class DividendPayment():
    def __init__(self,symbol, date, amt):
        self.symbol = symbol
        self.date = date
        self.dividend_amt = amt
    


class HistoricQuote():
    
    def __init__(self):
        self.symbol=None
        self.date=None
        self.open=None
        self.high=None
        self.low=None 
        self.close=None 
        self.volume = None 
    
    def day_change_percent(self):
        return (self.close - self.open)/self.open *100
    
    def day_spread_percent(self):
        return (self.high-self.low )/self.open * 100
    def __repr__(self):
        ret_str = []
        ret_str.append("Symbol: {0}, ".format(self.symbol))
        ret_str.append("Date: {0}, ".format(self.date))
        ret_str.append("Open: {0}, ".format(self.open))
        ret_str.append("High: {0}, ".format(self.high))
        ret_str.append("Low: {0}, ".format(self.low))
        ret_str.append("Close: {0}, ".format(self.close))
        ret_str.append("Volume: {0}, ".format(self.volume))
        return ''.join(ret_str)

class CompanyOverview():
    
    def __init__(self):
        self.symbol=None
        self.name=None 
        self.lastsale=None 
        self.marketcap=None 
        self.ipoyear=None 
        self.sector=None 
        self.industry=None 
        self.summary_quote=None 

    def parse_market_cap(self,marketcap):
        """parse the market cap string to a number"""
        marketcap=marketcap.replace('$','').strip()
        if marketcap.endswith('M'):
            factor=1000000
            marketcap=marketcap.replace('M','')
            return (float)(marketcap) *factor
        elif marketcap.endswith('B'):
            factor=1000000000
            marketcap=marketcap.replace('B','')
            return (float)(marketcap) *factor
        
    def __repr__(self):
        ret_str = []
        ret_str.append("Symbol: {0}, ".format(self.symbol)) 
        ret_str.append("Name: {0}, ".format(self.name))
        ret_str.append("Last Sale: {0}, ".format(self.lastsale))
        ret_str.append("Market Cap: {0}, ".format(self.marketcap))
        ret_str.append("IPO Year: {0}, ".format(self.ipoyear))
        ret_str.append("Sector: {0}, ".format(self.sector))
        ret_str.append("Industry: {0}, ".format(self.industry))
        ret_str.append("Summary Quote: {0}".format(self.summary_quote))
        return ''.join(ret_str)
    