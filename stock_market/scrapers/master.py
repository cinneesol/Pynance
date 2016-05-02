from company_overviews import scrape_exchange_listings
from scrape_historic_quotes import scrape_historic_quotes
from historic_quote_analysis import analyze
from csv import DictWriter
from multiprocessing import Pool, Pipe
import os


def process_work(args):
    company, conn = args
    try:
        analysis = analyze(company["Symbol"],None)
        conn.send(analysis)
    except Exception as e:
        print("Error for "+company["Symbol"])
        
if __name__=="__main__":
    analysis_results = []
    companies = scrape_exchange_listings()
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
        parent, child = Pipe()
        with Pool(os.cpu_count()) as pool:
            pool.map(process_work, [(x,child) for x in companies])
        
        while parent.poll(20):
            result = parent.recv()
            writer.writerow(result)