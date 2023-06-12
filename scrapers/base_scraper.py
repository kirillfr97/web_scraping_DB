from abc import ABC, ABCMeta, abstractmethod

from typing import List
from requests import Session
from datetime import datetime
from pandas import DataFrame, concat
from bs4 import BeautifulSoup as BSoup

from utils.mongo import MongoData


class BaseScraper(ABC, metaclass=ABCMeta):
    """Base class for web scrapers.

    This class defines the common functionality and abstract methods for web scrapers.
    Subclasses must implement the abstract methods and provide values for the required attributes.

    """

    def __init__(self):
        """Initialize the BaseScraper object.

        Initializes an empty DataFrame to store scraped data.

        """
        self._data: DataFrame = DataFrame(columns=[
            MongoData.Title,
            MongoData.Link,
            MongoData.Time
        ])

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the web scraper. """
        pass

    @property
    @abstractmethod
    def target_url(self) -> str:
        """The target website or domain for scraping. """
        pass

    @property
    @abstractmethod
    def crawl_urls(self) -> List[str]:
        """The list of URLs to crawl and scrape data from. """
        pass

    @abstractmethod
    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        """Scrape a web page and extract relevant data.

        This is an abstract method that must be implemented by subclasses.
        It takes a BeautifulSoup object representing a web page and returns a DataFrame with scraped data.

        Args:
            web_page (BSoup): The BeautifulSoup object representing the web page to be scraped.

        Returns:
            DataFrame: A DataFrame containing the scraped data.

        """
        pass

    @staticmethod
    def _get_article_time() -> str:
        """Get the current time with UTC offset.

        Returns:
            str: The current time with UTC offset in the format 'YYYY-MM-DD UTC HH:MM'.

        """
        return datetime.now().strftime('%Y-%m-%d UTC %H:%M')

    def start(self) -> DataFrame:
        """Scrape data from a web pages provided in 'crawl_urls' attribute.

        Returns:
            DataFrame: The scraped data as a DataFrame.

        """
        # List of scraped data
        scraped_data: List[DataFrame] = []

        # Scrape through all URLs in the given list
        for crawl_url in self.crawl_urls:
            # Create a session object
            session = Session()

            # Send a GET request to the specified URL with a custom User-Agent header
            response = session.get(crawl_url, headers={'User-Agent': 'Mozilla/5.0'})

            # Close session
            session.close()

            if not response.ok:
                print(f'<{response.status_code}> Error occurred while connecting to {crawl_url}')
                continue

            # Invoke the provided function on the parsed page and return the result
            print(f'Scraping page {crawl_url}')
            new_data = self._scrape_page(BSoup(response.text, 'html.parser'))

            if new_data.empty:
                print(f'Received an empty DataFrame: nothing were found')
                continue

            # Appending found data to 'scraped_data'
            print(f'Scrape completed: found {len(new_data)} elements on the page')
            scraped_data.append(new_data)

        if len(scraped_data) == 0:
            print(f'No data were scraped from {self.target_url}')
            return DataFrame()
        return concat(scraped_data, ignore_index=True)
