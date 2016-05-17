from scrapers.nasdaq import exchange_listings, option_chain
from scrapers.investopedia import historic_quotes
from analysis.historic_quote_analysis import analyze
from multiprocessing import Pool
import json
import sqlite3
import dbprops
import time
import os
import sys

def process_work(company):
    """returns analysis of recent historic quotes for company."""
    analysis=None
    try:
        quotes = historic_quotes(company["Symbol"])
        analysis = analyze(quotes)
    except Exception as e:
        print("Error for historic quote analysis for  "+company["Symbol"]+" - "+str(e))
        return None    
    return analysis

def generate_input_tuples(results):
    """generates a tuple list for each analytic result to insert rows properly in an sqlite insertmany operation"""
    tuples = []
    for result in results:
        if result is not None:
            try:
                tuples.append((
                               result['Symbol'],
                               result['Date'],
                               result['avg_day_high'],
                               result['avg_day_low'],
                               result['avg_volume'],
                               result['day_high_std_dev'],
                               result['day_high_slope'],
                               result['day_low_std_dev'],
                               result['day_low_slope'],
                               result['avg_close'],
                               result['close_slope'],
                               result['close_std_dev'],
                               result['avg_dip'],
                               result['avg_jump'],
                               result['dip_std_dev'],
                               result['jump_std_dev'],
                               result['volume_weighted_avg_close'],
                               result['target_entry_price'],
                               result['target_exit_price'],
                               result['last_quote']['Close']
                               ))
            except Exception as e:
                print(str(e))
    return tuples 
        
if __name__=="__main__":
    
    companies = exchange_listings()
    processes = os.cpu_count()
    results = []
    with Pool(processes) as p:
        results.extend(p.map(process_work, [x for x in companies]))
     
    print("Results: "+str(len(results)))
    
    try:
        db = sqlite3.connect(dbprops.sqlite_file)
        db_cur = db.cursor()
        db_cur.execute("""
          CREATE TABLE IF NOT EXISTS historic_analytic(
           symbol text,
           date text,
           avg_day_high real,
           avg_day_low real,
           avg_volume real,
           day_high_std_dev real,
           day_high_slope real,
           day_low_std_dev real,
           day_low_slope real,
           avg_close real,
           close_slope real,
           close_std_dev real,
           avg_dip real,
           avg_jump real,
           dip_std_dev real,
           jump_std real,
           volume_weighted_avg_close real,
           target_entry_price real,
           target_exit_price real,
           last_close real,
           PRIMARY KEY (SYMBOL,DATE)
           )"""           
        )
        
        tuple_list = generate_input_tuples(results)
        db_cur.executemany("""
        INSERT OR REPLACE INTO historic_analytic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        tuple_list)
        db.commit()
    except Exception as e:
        print(str(e))
    print("TIme to run main function: "+str(time.process_time()))