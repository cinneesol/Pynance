
from datetime import datetime

class PynanceModel(object):
    def getInsertStatement(self):
        insert = """INSERT INTO """
        insert += str(self.__class__.__name__.lower())+" ("
        argc = 0
        for v in vars(self):
            if argc < len(vars(self))-1:
                insert += v.lower()+", "
                argc = argc+1
            else:
                insert += v.lower()+") "
                argc = argc+1
        insert += "VALUES("
        for v in vars(self):
            if argc>1:
               insert += "?,"
               argc = argc-1
            else:
               insert += "?)"
               argc = argc-1
        return insert 
        
        
        return insert
class DividendPayment(PynanceModel):
    def __init__(self,symbol, date, amt):
        self.symbol = symbol
        self.date = date
        self.dividend_amt = amt
    


class HistoricQuote(PynanceModel):
    
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
    

class CompanyOverview(PynanceModel):
    
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
if __name__=='__main__':
    p= CompanyOverview("asdf","asdf""asdf","asdf""asdf","asdf""asdf","asdf","asdf","asdf","asdf");
    print(tuple(p))