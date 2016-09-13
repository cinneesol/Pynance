"""
Update these to the appropriate database properties for your environment
to connect remotely for a postgresql database
"""
postgres_host='192.168.0.13'
postgres_port=5432
postgres_database='stockdata'
postgres_user='stockdata'
postgres_password='st0ckdata'
"""
use this if you wish to instead specify a local sqlite db Store 

"""
sqlite_file='C:\\Users\\rcove\\SoftwareDev\\database\\sqlite\\stockdata.db'


"""
Database queries
"""

sqlite3_create_company_overview = """
  CREATE TABLE IF NOT EXISTS company_overview(
      symbol text,
      name text,
      lastsale numeric,
      marketcap numeric,
      ipoyear text,
      sector text,
      industry text,
      summary_quote text,
      PRIMARY KEY(symbol,name)
      )
"""
sqlite3_drop_company_overviews = """
  DROP TABLE IF EXISTS company_overview;
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
           floating_shares_ratio real,
           PRIMARY KEY (SYMBOL,DATE)
           )"""
sqlite3_insert_historic_analytic = """
        INSERT OR REPLACE INTO historic_analytic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        
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

sqlite3_create_dividend_history = """
CREATE TABLE IF NOT EXISTS dividend_history(
 symbol TEXT,
 date TEXT,
 dividend_amt NUMERIC,
 PRIMARY KEY(symbol, date)
)
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
        h.avg_close
        FROM historic_analytic h
        WHERE h.date=(SELECT MAX(date) FROM historic_analytic)
        AND h.close_slope >0
        AND h.day_low_slope > 0
        AND h.day_high_slope >0
        AND h.avg_volume>100000
        AND avg_close <=volume_weighted_avg_close
            
    """
sqlite3_find_bottoming_out_reversal ="""
SELECT h.symbol,
        h.date,
        h.avg_day_high,
        h.avg_day_low,
        h.avg_close
        FROM historic_analytic h
        WHERE h.date=(SELECT MAX(date) FROM historic_analytic)
        AND h.close_slope <0
        AND h.day_low_slope > 0
        AND h.day_high_slope >0
        AND h.avg_volume>100000
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
    
sqlite3_find_company_profile_symbol="""
    SELECT * 
    FROM company_overview 
    WHERE symbol=? 
    OR name = (
        SELECT name
        FROM company_overview
        WHERE symbol=?
        )
    """
sqlite3_find_company_profile_name="""
    SELECT * 
    FROM company_overview 
    WHERE name LIKE ?
    """
    
    
sqlite3_count_dividends_symbol_date="""
SELECT COUNT(*),
FROM DIVIDEND_HISTORY DH 
WHERE DATE>=?
AND SYMBOL=?
"""
    
sqlite3_query_most_dividend_payments_date = """
SELECT CO.SYMBOL,
   CO.NAME,
   CO.LASTSALE,
   CO.INDUSTRY,
   DH.DATE, ((DH.DIVIDEND_AMT/CO.LASTSALE) * 100) AS YIELD,
   count(DH.SYMBOL) NUM_DIVS
 FROM DIVIDEND_HISTORY DH 
 JOIN COMPANY_OVERVIEW CO 
 ON DH.SYMBOL = CO.SYMBOL
 COLLATE NOCASE
 WHERE DATE >= ?
  group by (DH.SYMBOL)
 ORDER BY NUM_DIVS DESC
 """
 
  
sqlite3_query_dividend_payment_amounts_industry="""
SELECT CO.SYMBOL,
   CO.NAME,
   CO.LASTSALE,
   CO.INDUSTRY,
   DH.DATE, ((DH.DIVIDEND_AMT/CO.LASTSALE) * 100) AS YIELD,
   count(DH.SYMBOL) NUM_DIVS
 FROM DIVIDEND_HISTORY DH 
 JOIN COMPANY_OVERVIEW CO 
 ON DH.SYMBOL = CO.SYMBOL
  COLLATE NOCASE
 WHERE CO.INDUSTRY LIKE '%bank%'
 AND DH.DATE >='2010'
  group by (DH.SYMBOL)
  HAVING NUM_DIVS>=24
 ORDER BY NUM_DIVS DESC
"""

sqlite3_query_low_float_potential_rebounds = """
SELECT *
FROM historic_analytic 
where floating_shares_ratio <10
AND DATE = (SELECT MAX(DATE) FROM historic_analytic)
AND avg_volume > 100000
AND day_high_slope>0
AND day_low_slope>0
AND close_slope>0
"""

