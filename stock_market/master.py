from scrapers.nasdaq import exchange_listings, option_chain
from scrapers.investopedia import historic_quotes
from historic_quote_analysis import analyze
from multiprocessing import Pool
import json
from pg import DB
import dbprops
import time
import os
import sys

def process_work(company):
    analysis=None
    try:
        quotes = historic_quotes(company["Symbol"])
        analysis = analyze(quotes)
    except Exception as e:
        print("Error for historic quote analysis for  "+company["Symbol"]+" - "+str(e))
        return None    
    return analysis

if __name__=="__main__":
    
    companies = exchange_listings()
    processes = os.cpu_count()
    results = []
    with Pool(processes) as p:
        results.extend(p.map(process_work, [x for x in companies]))
     
    print("Results: "+str(len(results)))
    try:
        postgres = DB(host=dbprops.host, dbname=dbprops.database, 
                      port=dbprops.port, user=dbprops.user, passwd=dbprops.password)
        for result in results:
            if result is not None:
                try:
                    result["Date"] = result["Date"].isoformat()
                    result["last_quote"]["Date"]=result["last_quote"]["Date"].isoformat() 
                    postgres.insert('historic_analytic', data=result)
                except Exception as e:
                    print(str(e))
                    
        
    finally:
        postgres.close()
    print("TIme to run main function: "+str(time.process_time()))