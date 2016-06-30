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
sqlite_file="stockdata.db"



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