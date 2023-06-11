from abc import ABC, ABCMeta, abstractmethod
from bs4.element import PageElement, ResultSet
from bs4 import BeautifulSoup as BSoup, Tag
from typing import Optional, Tuple
from re import compile, findall
from datetime import datetime
from pandas import DataFrame
from requests import Session

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

    def __init_subclass__(cls, **kwargs):
        """Special method called when a subclass of BaseScraper is defined.

        This method checks if the subclass provides values for the required attributes.

        Args:
            **kwargs: Additional keyword arguments.

        Raises:
            NotImplementedError: If the subclass does not provide a value for any of the required attributes.

        """
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'target_url'):
            raise NotImplementedError('Subclasses must provide a value for "target_url" attribute.')
        if not hasattr(cls, 'crawl_url'):
            raise NotImplementedError('Subclasses must provide a value for "crawl_url" attribute.')
        if not hasattr(cls, 'name'):
            raise NotImplementedError('Subclasses must provide a value for "name" attribute.')

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
    def crawl_url(self) -> str:
        """The URL to crawl and scrape data from. """
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

    def _get_lnk_title(self, tag: Tag | PageElement, regex: str = r'https\S*') -> Tuple[Optional[str], Optional[str]]:
        """Extract the link and title from a given tag.

        This method extracts the link and title from the given tag based on the specified regex pattern.

        Args:
            tag (Tag | PageElement): The BeautifulSoup Tag or PageElement object to extract the link and title from.
            regex (str): The regular expression pattern to match the link.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the extracted link and title,
            or (None, None) if not found.

        """
        # Find all tags within the given tag that match the specified regex pattern
        sections: ResultSet = tag.find_all('a', attrs={'href': compile(regex)})

        # Iterate over the found tags
        for section in sections:
            lnk = section.get('href')  # Extract the link
            title = section.text  # Extract the title
            if lnk != '' and title != '':
                # if it doesn't contain the full URL
                if len(findall(r'https\S*', lnk)) == 0:
                    # Prepend the target_url to the link
                    lnk = self.target_url + lnk
                return lnk, title.replace('â€™', '\'')
        return None, None

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
            raise Exception(f'<{response.status_code}> Error occurred while connecting to {self.crawl_url}')

        print(f'Scraping page {self.crawl_url}')

        # Invoke the provided 'method' function on the parsed page and return the result
        scraped_data = self._scrape_page(BSoup(response.text, 'html.parser'))

        print(f'Scrape completed: found {len(scraped_data)} elements on the page')

        if scraped_data.empty:
            raise Exception('Received an empty DataFrame while scraping')

        return scraped_data


if __name__ == '__main__':
    from bloomberg import BloombergScraper as SelectedScraper
    # from cnbc import CNBCScraper as SelectedScraper

    # Create selected scraper
    scraper: BaseScraper = SelectedScraper()

    # Scrape the web-page
    page_data = scraper.start()

    print(page_data[MongoData.Title].values)
