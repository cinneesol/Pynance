# Pynance
mega-project containing python scripts and programs to handle all things finance


Dependendent packages for stock market data scraping:
lxml 3.4.4
BeautifulSoup 4




#Current Features
    New features will be built and released as soon as possible. 
    v 0.2.3:
        -added Yahoo finance floating shares scraping function
        -added Yahoo finance dividend history scraping function
        -added floating shares ratio to historic quote analysis
        -added scraping functions for getting news articles for a stock from investopedia.com
        -added scraping functions for scraping news articles for a stock from nasdaq.com
        
    v 0.2.2:
        -package restructuring
        -cleaning up test and demo files
        -adding yahoo finance historical data scraper
        
    v 0.2.1:
        -added property to determine whether or not to scrape options data
          with the historical quote scrape on the master scraper script
        -added scraper to retrieve dividend history information from investopedia.com
        
    v 0.2.0:
        -added Django and AngularJS powered web UI for viewing stock data 
           related information
        -added web view for searching uptrending stocks by their target entry and 
           target profit percentage
           
    v 0.1.1:
        -scraper for retrieving options data from www.investopedia.com
    
    v 0.1.0:
        - cli for home budget analysis
        - scraper for company overviews from www.nasdaq.com
        - scraper for retrieving historic quotes from www.investopedia.com
        - statistical analysis for historic quotes from a given company
        - master script for stock market data retriever and analyzer
    
    
### To use these modules in your own scripts:
To use scraping and analytic features in your own scripts(Make sure that Pynance folder is in your PYTHONPATH): 

get a list of companies and their information from the NYSE,AMEX,and NASDAQ exchanges:
```
 from Pynance.stock_market.scrapers.nasdaq import exchange_listings
 
 companies = exchange_listings() 
```
getting historic quotes for a company: 
```
 from Pynance.stock_market.scrapers.investopedia import historic_quotes 
 
 microsoft_quotes = historic_quotes('MSFT')
```
getting options information for a company
```
 from Pynance.stock_market.scrapers.investopedia import option_chain
 
 microsoft_options_data = option_chain('MSFT')
```

analyzing historic quote statistics for a company
```
 from Pynance.stock_market.scrapers.investopedia import historic_quotes 
 from Pynance.stock_market.analysis.historic_quote_analysis import analyze
 
 historic_statistical_analysis = analyze(historic_quotes('MSFT'))
```
    
###To run the Pynance Django web server
To run the Pynance web server, open a command window in the web_ui folder and run manage.py with the first parameter
being 'runserver' and the second being an optional parameter
for the port that you wish the server to be bound to. For example, to run the server off of port 8080:

```
python manage.py runserver 8080
```     
This will launch the Django server listening on port 8080. Hitting http://localhost:8080/stockdata will take 
you to the home page for the stock data web app on the Django server.
