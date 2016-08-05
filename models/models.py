from django.db.models.functions import Lower

class DividendPayment(object):
    def __init__(self,symbol, date, amt):
        self.symbol = symbol.lower()
        self.date = date.lower()
        self.dividend_amt = amt


class HistoricQuote(object):
    
    def __init__(self, symbol, date, open, high, low, close, volume):
        self.symbol=symbol
        self.date=date
        self.open=open
        self.high=high
        self.low=low 
        self.close=close 
        self.volume = volume 
    
    def day_change_percent(self):
        return (self.close - self.open)
    
    def day_spread_percent(self):
        return self.high-self.low 
    

class CompanyOverview(object):
    
    def __init__(self,symbol,name,lastsale,marketcap,ipoyear,sector,industry,summary_quote):
        self.symbol=symbol
        self.name=name 
        self.lastsale=lastsale 
        self.marketcap=marketcap 
        self.ipoyear=ipoyear 
        self.sector=sector 
        self.industry=industry 
        self.summary_quote=summary_quote 

