from time import sleep
from pandas import DataFrame
from requests import Session
from bs4 import BeautifulSoup as BSoup

from utils.mongo import MongoDataBase
from utils.slack import message_to_slack
from scrapers.bloomberg import bloomberg
from config.helpers import get_time_interval


def scrape(url: str, method) -> DataFrame:
    """Scrape data from a web page using the specified method.

    Args:
        url (str): The URL of the web page to scrape.
        method: The method to invoke on the parsed page.

    Returns:
        DataFrame: The scraped data as a DataFrame.

    Raises:
        Exception: If an error occurs while connecting to the URL or if the scraped DataFrame is empty.

    """
    # Create a session object
    session = Session()

    # Send a GET request to the specified URL with a custom User-Agent header
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Close session
    session.close()

    if not response.ok:
        raise Exception(f'<{response.status_code}> Error occurred while connecting to {url}')

    # Invoke the provided 'method' function on the parsed page and return the result
    print(f'Scraping page {url}')
    scraped = method(BSoup(response.text, 'html.parser'))
    print(f'Scrape completed: found {len(scraped)} elements on the page')

    if scraped.empty:
        raise Exception('Received an empty DataFrame while scraping')

    return scraped


if __name__ == "__main__":

    print('Connecting to Database...')

    # Establish a connection to the MongoDB cluster
    cluster = MongoDataBase()

    try:
        # Endless River
        while True:
            # Scrape the Bloomberg web-page using the 'bloomberg' method
            page_data = scrape('https://www.bloomberg.com/economics', bloomberg)

            # Update the MongoDB database with the scraped data and retrieve the message
            cluster.update(data=page_data, collection_name='Bloomberg')

            # Send the message to Slack
            message_to_slack(cluster.message)

            # Sleep
            sleep(get_time_interval())
            print(f'Sleep for {get_time_interval() // 60} min...\n')

    except Exception as e:
        # Handle other exceptions
        print(repr(e))

    finally:
        # Close the connection to the MongoDB cluster
        # noinspection PyUnboundLocalVariable
        cluster.close()
