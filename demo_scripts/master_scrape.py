from Pynance.stock_market.scrapers.nasdaq import exchange_listings, option_chain
from Pynance.stock_market.scrapers.investopedia import historic_quotes, option_chain
from Pynance.stock_market.analysis.historic_quote_analysis import analyze
from Pynance.stock_market.analysis.options_analysis import analyze_options
from Pynance.stock_market.scrapers.yahoo_finance import floating_outstanding_shares
from multiprocessing import Pool
import json
import sqlite3
from Pynance.database import dbprops
from Pynance.database import db_util
import time
import os
import sys

#TODO: get rid of global options flag
include_options=False

def process_work(company):
    """returns analysis of recent historic quotes for company."""
    analysis=None
    try:
        quotes = historic_quotes(company.symbol)
        floating_shares = floating_outstanding_shares(company.symbol)
        analysis = analyze(quotes, floating_shares)
    except Exception as e:
        print("Error for historic quote analysis for  "+company["Symbol"]+" - "+str(e))
        return None    
    if include_options:
        try:
            analysis['option_chain_analysis']=analyze_options(option_chain(company["Symbol"].lower()))
        except Exception as e:
            print("Error for option chain analysis for "+company['Symbol']+ " - "+str(e))
            analysis['option_chain_analysis']=None
    return analysis

def generate_historic_analytic_input_tuples(results):
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
                               result['last_quote']['Close'],
                               result['floating_shares_ratio']
                               ))
            except Exception as e:
                print(str(e))
    return tuples 
        
def generate_options_input_tuples(results):
    tuples = []
    for result in results:
        if result is not None:
            if result['option_chain_analysis'] is not None:
                option_analysis = result['option_chain_analysis']
                for month in option_analysis['month_analysis'].keys():
                    tuples.append(
                                  (option_analysis['symbol'],
                                   option_analysis['date'],
                                   month,
                                   option_analysis['month_analysis'][month]['weighted_effective_put_price'],
                                   option_analysis['month_analysis'][month]['weighted_effective_call_price'],
                                   )
                                  )
    return tuples

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=='include-options':
        include_options=True
    else:
        include_options=False
        
    companies = exchange_listings()
    print(companies[1])
    sys.exit()
    processes = os.cpu_count()
    results = []
    with Pool(processes) as p:
        results.extend(p.map(process_work, [x for x in companies]))
      
    print("Results: "+str(len(results)))
    
    try:
        db = sqlite3.connect(dbprops.sqlite_file)
        db_cur = db.cursor()
        db_cur.execute(dbprops.sqlite3_create_historic_analytic)
        db_cur.execute(dbprops.sqlite3_create_option_analysis)
        #we want to remove and recreate the company overview table with each run
        db_cur.execute(dbprops.sqlite3_drop_company_overviews)
        db_cur.execute(dbprops.sqlite3_create_company_overview)
        db_cur.execute("BEGIN TRANSACTION")
        for company in companies:
            try:
                db_util.insert(table="company_overview",conn=db, data=company)
                
            except:
                print("error")
                #TODO log error
        db.commit()
        historic_analysis_tuple_list = generate_historic_analytic_input_tuples(results)
        if include_options:
            options_analysis_tuple_list = generate_options_input_tuples(results)
        
        #begin transaction for executing historic analytic table
        db_cur.execute("BEGIN TRANSACTION")
        db_cur.executemany(dbprops.sqlite3_insert_historic_analytic,
        historic_analysis_tuple_list)
        db.commit()
        if include_options:
            #begin transaction for options analysis insert
            db_cur.execute("BEGIN TRANSACTION")
            db_cur.executemany(dbprops.sqlite3_insert_option_analysis,options_analysis_tuple_list)
            db.commit()
    except Exception as e:
        print(str(e))
    print("Finished scraping and analyzing stock market data")
    