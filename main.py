from time import sleep
from pandas import DataFrame
from requests import Session
from bs4 import BeautifulSoup as BSoup

from scrapers.bloomberg import bloomberg
from utils.slack import message_to_slack
from utils.mongo import update_mongo
from config.settings import TIME_INTERVAL
from config.helpers import get_mongo_cluster


def scrape(url: str, method) -> DataFrame:
    # Create a session object
    session = Session()

    # Send a GET request to the specified URL with a custom User-Agent header
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Parse the response content using BeautifulSoup with the 'html.parser' parser
    page = BSoup(response.text, 'html.parser')

    # Invoke the provided 'method' function on the parsed page and return the result
    return method(page)


if __name__ == "__main__":
    # Endless River
    while True:
        # Scrape the Bloomberg web-page using the 'bloomberg' method
        web_page = scrape('https://www.bloomberg.com/economics', bloomberg)

        # Getting the MongoDB cluster URL
        cluster_url = get_mongo_cluster()

        # Update the MongoDB database with the scraped data and retrieve the message
        message = update_mongo(cluster_url, web_page)

        # Send the message to Slack
        message_to_slack(message if message != '' else 'Nothing new yet...')

        # Sleep
        sleep(TIME_INTERVAL)
