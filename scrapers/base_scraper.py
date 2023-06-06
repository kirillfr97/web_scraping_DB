from abc import ABC, ABCMeta, abstractmethod

from bs4 import BeautifulSoup as BSoup
from pandas import DataFrame
from requests import Session


class BaseScraper(ABC, metaclass=ABCMeta):

    name: str
    crawl_url: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'crawl_url', None):
            raise NotImplementedError('Subclasses must provide a value for \"crawl_url\" attribute.')
        if not getattr(cls, 'name', None):
            raise NotImplementedError('Subclasses must provide a value for \"name\" attribute.')

    @abstractmethod
    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        pass

    def start(self) -> DataFrame:
        """Scrape data from a web page provided in 'crawl_url' attribute.

        Returns:
            DataFrame: The scraped data as a DataFrame.

        Raises:
            Exception: If an error occurs while connecting to the URL or if the scraped DataFrame is empty.

        """
        # Create a session object
        session = Session()

        # Send a GET request to the specified URL with a custom User-Agent header
        response = session.get(self.crawl_url, headers={'User-Agent': 'Mozilla/5.0'})

        # Close session
        session.close()

        if not response.ok:
            raise Exception(f'<{response.status_code}> Error occurred while connecting to {url}')

        print(f'Scraping page {self.crawl_url}')

        # Invoke the provided 'method' function on the parsed page and return the result
        data = self._scrape_page(BSoup(response.text, 'html.parser'))

        print(f'Scrape completed: found {len(data)} elements on the page')

        if data.empty:
            raise Exception('Received an empty DataFrame while scraping')

        return data
