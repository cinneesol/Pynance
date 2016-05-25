import sqlite3 



def get_nearby_stocks(percent):
    db = sqlite3.connect("stockdata.db")
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute("""
       SELECT symbol,
       date,
       last_close,
       target_entry_price,
       target_exit_price, 
       avg_day_high,
       avg_day_low,
       avg_close,
       avg_dip,
       dip_std_dev
       FROM historic_analytic 
       WHERE date =(SELECT MAX(date) FROM historic_analytic) 
       AND target_entry_price < target_exit_price
       AND ABS(target_exit_price-target_entry_price)/target_entry_price > .015
       AND ABS(target_entry_price-last_close)/last_close <= ?
       AND close_slope > 0
       AND day_low_slope >0
       AND day_high_slope > 0
       AND avg_volume>50000
       AND last_close>10
       AND avg_close <=volume_weighted_avg_close
       
       """, (percent,))
    
    results = []
    for r in c.fetchall():
        results.append(r)
    return results

if __name__=='__main__':
    percent_away = input("How far away(% multiplier) from target entry point? \n")
    print("running query...")
    results = get_nearby_stocks(percent=percent_away)
    for stock in results:
        result = {}
        for field in stock.keys():
            if field.lower() in ('symbol', 'date', 'target_entry_price','target_exit_price'):
                result[field]=stock[field]
        print(result)
    print(len(results))