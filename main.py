from time import sleep
from pandas import DataFrame
from requests import Session
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bs4 import BeautifulSoup as BSoup

from scrapers.bloomberg import bloomberg
from utils.slack import message_to_slack
from utils.mongo import update_mongo
from config.settings import TIME_INTERVAL
from config.helpers import get_mongo_cluster


class EmptyDataException(Exception):
    pass


class NoAvailableCluster(Exception):
    pass


def scrape(url: str, method) -> DataFrame:
    # Create a session object
    session = Session()
    print('Starting a new session...')

    # Send a GET request to the specified URL with a custom User-Agent header
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if not response.ok:
        print(f'<{response.status_code}> Error occurred while connecting to {url}')
        return DataFrame()

    # Parse the response content using BeautifulSoup with the 'html.parser' parser
    page = BSoup(response.text, 'html.parser')

    # Close session
    session.close()

    # Invoke the provided 'method' function on the parsed page and return the result
    return method(page)


if __name__ == "__main__":

    print('Connecting to Database...')
    try:
        # Getting the MongoDB cluster URL
        cluster_url = get_mongo_cluster()
        if cluster_url is None:
            raise NoAvailableCluster('No MongoDB cluster were found')

        # Establish a connection to the MongoDB cluster
        cluster: MongoClient = MongoClient(cluster_url)

        # Low cost check to verify the availability of the MongoDB server
        cluster.admin.command('ping')

        # Get the 'News' database
        database = cluster['News']

        # Endless River
        while True:
            # Scrape the Bloomberg web-page using the 'bloomberg' method
            page_data = scrape('https://www.bloomberg.com/economics', bloomberg)
            if page_data.empty:
                raise EmptyDataException('Received an empty DataFrame while scraping')

            # Update the MongoDB database with the scraped data and retrieve the message
            message = update_mongo(database=database, collection_name='Bloomberg', data=page_data)

            # Send the message to Slack
            message_to_slack(message if message != '' else 'Nothing new yet...')

            # Sleep
            sleep(TIME_INTERVAL)
            print('\n')

    except ConnectionFailure:
        # Handle connection failure error
        print('Server not available')

    except Exception as error:
        # Handle other exceptions
        print(repr(error))

    finally:
        # Close the connection to the MongoDB cluster
        # noinspection PyUnboundLocalVariable
        cluster.close()
