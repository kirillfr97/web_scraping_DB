from pandas import DataFrame
from requests import Session
from bs4 import BeautifulSoup as BSoup

from scraping.bloomberg import bloomberg
from config.helpers import get_mongo_cluster
from utils.slack import message_to_slack
from utils.mongo import update_mongo


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
    # Scrape the Bloomberg web-page using the 'bloomberg' method
    bb = scrape('https://www.bloomberg.com/economics', bloomberg)

    # Update the MongoDB database with the scraped data and retrieve the message
    message = update_mongo(get_mongo_cluster(), bb)

    # Send the message to Slack
    message_to_slack(message if message != '' else 'Nothing new yet...')


