from company_overviews import scrape_exchange_listings
from scrape_historic_quotes import scrape_historic_quotes





if __name__=="__main__":
    companies = scrape_exchange_listings()
    print("Retrieved "+str(len(companies))+" companies from exchanges")
    quotes = []
    for company in companies:
        print("Scraping quotes for "+company["Symbol"])
        try:
            historic_quotes= scrape_historic_quotes(company["Symbol"])
            print("Found "+str(len(historic_quotes))+" quotes")
            quotes.extend(historic_quotes)
        except:
            print("Failed getting quotes for "+company["Symbol"])
    print(str(len(quotes))+" total historic quotes scraped")