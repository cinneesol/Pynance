from Pynance.database import dbprops
from Pynance.stock_market.scrapers import investopedia
from Pynance.stock_market.scrapers import nasdaq

import sqlite3
import json 
import datetime
from Pynance.stock_market.scrapers.investopedia import dividend_history



def initialize_dividend_table():
    with sqlite3.connect(dbprops.sqlite_file) as conn:
        cursor = conn.cursor()
        cursor.execute(dbprops.sqlite3_create_dividend_history)
        conn.commit()
    
def save_dividend_history(dividend_payments):
    records =[]
    for payment in dividend_payments:
        records.append((payment.symbol.upper(),payment.date.isoformat(),payment.dividend_amt)) 
        
    if len(records)>0:
        with sqlite3.connect(dbprops.sqlite_file) as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            statement = cursor.executemany("""
            INSERT OR IGNORE INTO dividend_history(symbol,date,dividend_amt) VALUES(?,?,?) """,
            records)
            conn.commit()
            print("Successfully saved or updated  "+str(len(records))+" records for "+dividend_payments[0].symbol)
        
if __name__=='__main__':
    initialize_dividend_table()
    companies = nasdaq.exchange_listings()
    for company in companies:
        try:
            company_dividends = dividend_history(company['Symbol'])
            save_dividend_history(company_dividends)
        except Exception as e:
            print("failed to save dividend history for "+company['Symbol'])
            
        