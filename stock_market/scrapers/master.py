from company_overviews import scrape_exchange_listings
from scrape_historic_quotes import scrape_historic_quotes
from historic_quote_analysis import analyze
from csv import DictWriter
from multiprocessing import Process, Queue, Pool
import os


def process_work(company):
    try:
        quotes = scrape_historic_quotes(company["Symbol"])
        analysis = analyze(quotes)
        return analysis
    except Exception as e:
        print("Error for "+company["Symbol"]+" - "+str(e))
        return None

        
if __name__=="__main__":
    analysis_results = []
    companies = scrape_exchange_listings()
    processes = 6
    results = []
    with Pool(processes) as p:
        results.extend(p.map(process_work, [x for x in companies]))
    
    print("Results: "+str(len(results)))
    #start new csv file
    with open('analysis.csv','w') as csvfile:
        fieldnames = ['Symbol', 'Date','avg_day_high',
                     'avg_day_low',
                     'day_high_std_dev',
                      'day_low_std_dev',
                     'avg_close',
                      'close_std_dev',
                     'avg_dip',
                     'avg_jump',
                     'dip_std_dev',
                     'jump_std_dev',
                     'target_entry_price' ]
        writer = DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            if r is not None:
                writer.writerow(r)