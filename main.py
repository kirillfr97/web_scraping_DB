import json
from time import sleep

from utils.mongo import MongoDataBase
from utils.slack import message_to_slack
from config.helpers import get_time_interval
from scrapers.implicit_link_scraper import ImplicitLinkScraper


def read_json(filename: str) -> dict:
    print(f'Opening JSON file {filename}...')
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


# Establish a connection to the MongoDB cluster
cluster = MongoDataBase()

try:
    # Endless River
    while True:
        for _, scraper_info in read_json('test.json').items():
            # Creating scraper
            scraper = ImplicitLinkScraper(**scraper_info)

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
