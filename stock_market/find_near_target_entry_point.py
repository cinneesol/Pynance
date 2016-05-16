import sqlite3 



def get_nearby_stocks(percent,date):
    db = sqlite3.connect("stockdata.db")
    c = db.cursor()
    c.execute("""
       SELECT symbol,
       date,
       last_close,
       avg_day_high,
       avg_day_low,
       avg_close,
       avg_dip,
       dip_std_dev,
       target_entry_price 
       FROM historic_analytic 
       WHERE date =?
       AND ABS(target_entry_price-last_close)<= (target_entry_price * (?/100))
       AND volume_weighted_avg_close > avg_close
       """, (date,percent))
    
    results = []
    for r in c.fetchall():
        results.append(r)
    return results

if __name__=='__main__':
    percent_away = input("How far away(%) from target entry point? \n")
    target_date = input("Enter date in question in iso format (yyyy-mm-dd)\n")
    print("running query...")
    results = get_nearby_stocks(percent=percent_away, date=target_date)
    for stock in results:
        print(stock)
    