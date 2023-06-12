from time import sleep

from utils.mongo import MongoDataBase
from utils.slack import message_to_slack
from config.helpers import get_time_interval
from scrapers.cnbc import CNBCScraper
from scrapers.bloomberg import BloombergScraper
from scrapers.yahoo_finance import YahooFinanceScraper
from scrapers.financial_time import FinancialTimesScraper


# Establish a connection to the MongoDB cluster
cluster = MongoDataBase()

try:
    # Endless River
    while True:
        for scraper in [
            BloombergScraper(),
            CNBCScraper(),
            FinancialTimesScraper(),
            YahooFinanceScraper(),
        ]:
            # Scrape the web-page
            page_data = scraper.start()

            # Update the MongoDB database with the scraped data and retrieve the message
            cluster.update(data=page_data, collection_name=scraper.name)

            # Send the message to Slack
            message_to_slack(cluster.message)

        # Sleep
        sleep(get_time_interval())

except Exception as e:
    # Handle other exceptions
    print(repr(e))

finally:
    # Close the connection to the MongoDB cluster
    cluster.close()
