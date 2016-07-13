"""
Update these to the appropriate database properties for your environment
to connect remotely for a postgresql database
"""
# host='192.168.0.13'
# port=5432
# database='stockdata'
# user='stockdata'
# password='st0ckdata'
"""
use this if you wish to instead specify a local sqlite db Store 

"""
sqlite_file='C:\\Users\\rcove\\SoftwareDev\\database\\sqlite\\stockdata.db'



"""
Database queries
"""
sqlite3_create_historic_analytic = """
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
sqlite3_insert_historic_analytic = """
        INSERT OR REPLACE INTO historic_analytic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        
sqlite3_create_option_analysis = """
CREATE TABLE IF NOT EXISTS options_analysis(
symbol text,
date text,
option_month integer,
weighted_eff_put_price real,
weighted_eff_call_price real,
PRIMARY KEY (symbol,date,option_month)
)
"""

sqlite3_insert_option_analysis = """
INSERT OR REPLACE INTO options_analysis VALUES(?,?,?,?,?) 
"""

sqlite3_find_near_target_entry = """
           SELECT symbol,
           date,
           last_close,
           target_entry_price,
           target_exit_price, 
           avg_day_high,
           avg_day_low,
           avg_close,
           avg_dip,
           dip_std_dev,
           (ABS(target_entry_price-last_close)/last_close) as DISTANCE
           FROM historic_analytic 
           WHERE date =(SELECT MAX(date) FROM historic_analytic) 
           AND target_entry_price < target_exit_price
           AND ABS(target_exit_price-target_entry_price)/target_entry_price > ?
           AND DISTANCE <= ?
           AND close_slope > 0
           AND day_low_slope >0
           AND day_high_slope > 0
           AND avg_volume>1000000
           AND last_close>10
           AND avg_close <=volume_weighted_avg_close
           
           """
sqlite3_find_uptrend_historical_analysis = """
        SELECT h.symbol,
        h.date,
        h.avg_day_high,
        h.avg_day_low,
        h.avg_day_close
        FROM historic_analytic h
        WHERE h.date=(SELECT MAX(date) FROM historic_analytic)
        AND h.close_slope >0
        AND h.day_low_slope > 0
        AND h.day_high_slope >0
    """
    
sqlite3_find_upcoming_positive_options_analysis = """
        SELECT  o.symbol,
        o.date,
        o.option_month,
        o.weighted_eff_put_price,
        o.weighted_eff_call_price
        FROM options_analysis o
        WHERE o.date = (SELECT MAX(date) FROM options_analysis)
        AND o.weighted_eff_put_price <= o.weighted_eff_call_price
    """
