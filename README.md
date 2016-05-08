# Pynance
mega-project containing python scripts and programs to handle all things finance


Dependendent packages for stock market data scraping:
lxml 3.4.4
BeautifulSoup 4
Pygresql 5.0



#Current Features
    New features will be built and released as soon as possible. 
##v 0.1.0:
    - cli for home budget analysis
    - scraper for company overviews from www.nasdaq.com
    - scraper for retrieving historic quotes from www.investopedia.com
    - statistical analysis for historic quotes from a given company
    -master script for stock market data retriever and analyzer
    
    
## To use these modules in your own scripts:
    To use scraping and analytic features in your own scripts: 
    
    getting historic quotes for a company: 
    
    <code>
     from Pynance.stock_market.scrapers.historic_quotes import scrape 
     
     microsoft_quotes = scrape('MSFT')
    </code>
    
    analyzing historic quote statistics for a company
    <code>
     from Pynance.stock_market.scrapers.historic_quotes import scrape
     from Pynance.stock_market.analysis.historic_quote_analysis import analyze
     
     historic_statistical_analysis = analyze(scrape('MSFT'))
    </code>
    
     