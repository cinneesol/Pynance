
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
    
    def __init__(self,symbol,name,lastsale,marketcap,ipoyear,sector,industry,summary_quote):
        self.symbol=symbol
        self.name=name 
        self.lastsale=lastsale 
        self.marketcap=marketcap 
        self.ipoyear=ipoyear 
        self.sector=sector 
        self.industry=industry 
        self.summary_quote=summary_quote 



if __name__=='__main__':
    p= CompanyOverview("asdf","asdf""asdf","asdf""asdf","asdf""asdf","asdf","asdf","asdf","asdf");
    print(tuple(p))