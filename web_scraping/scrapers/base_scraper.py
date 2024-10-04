from abc import ABC, ABCMeta, abstractmethod
from typing import Hashable, List

from lxml.html import HtmlElement, fromstring
from pandas import DataFrame
from requests import Response

from web_scraping.log import CONTENT_KEY, LINK_KEY, UA_KEY, log
from web_scraping.utils import DataFields
from web_scraping.utils.response import defaultUA, get_response
from web_scraping.utils.unfurl import MetaExtractor


class BadResponseError(Exception):
    pass


class BaseScraper(ABC, metaclass=ABCMeta):
    """Base class for web scrapers.

    This class defines the common functionality and abstract methods for web scrapers.
    Subclasses must implement the abstract methods and provide values for the required attributes.

    """

    def __init__(self):
        """Initialize the BaseScraper object.

        Initializes an empty DataFrame to store scraped data.

        """
        # if True scraper will ALWAYS save response to the database
        self._debug_mode: bool = False
        # User_Agent used in GET request header
        self._user_agent: str = defaultUA
        # Current web page we are working with
        self._current_page: int = 0
        # Table to store scraped data from web pages
        self._data: DataFrame = DataFrame(columns=list(DataFields()))
        # Metadata extractor
        self._extractor = MetaExtractor()

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the web scraper."""
        pass

    @property
    @abstractmethod
    def target_url(self) -> str:
        """The target website or domain for scraping."""
        pass

    @property
    @abstractmethod
    def crawl_urls(self) -> List[str]:
        """The list of URLs to crawl and scrape data from."""
        pass

    @property
    def data(self) -> DataFrame:
        """Returns table with scraped data in it."""
        return self._data.copy()

    @property
    def current_url(self) -> str:
        """Returns current crawling url from the list."""
        if self._current_page < len(self.crawl_urls):
            return self.crawl_urls[self._current_page]
        return ''

    @abstractmethod
    def _scrape_page(self, web_page: HtmlElement):
        """Scrape a web page and extract relevant data into DataFrame.

        This is an abstract method that must be implemented by subclasses.
        It takes HTML representation of a web page and updates existing DataFrame with scraped data.

        Args:
            web_page (HtmlElement): The HTML representation of the web page to be scraped.

        """
        pass

    def _get_metadata(self, url: str, timeout: int = 15) -> dict:
        """Retrieve metadata for a given URL using unfurling.

        Args:
            url (str): The URL for which to retrieve metadata.
            timeout (int): The timeout value for the HTTP request in seconds. Defaults to 15.

        Returns:
            dict: A dictionary containing the unfurled metadata for the URL.

        """
        return self._extractor.unfurl(url=url, user_agent=self._user_agent, timeout=timeout)

    def add_metadata(self, row_idx: Hashable):
        """Add metadata to a specific row in the DataFrame.

        This method takes a row index as input, retrieves the corresponding row from the DataFrame,
        and updates it with metadata information obtained using the 'DataFields.Link' column.

        Args:
            row_idx (Hashable): The index of the row to be updated.

        """
        # Retrieve the row corresponding to the given row index
        row = self._data.loc[row_idx].copy()

        # Extract the metadata using the 'DataFields.Link' value as a key
        metadata = self._get_metadata(row[DataFields.Link])

        # Update the 'DataFields.Title' and 'DataFields.Description' columns with metadata values
        row[DataFields.Title] = metadata['title']
        row[DataFields.Description] = metadata['description']

        # Update the DataFrame with the modified row
        self._data.loc[row_idx] = row

    def start(self):
        """Scrape data from web pages provided in 'crawl_urls' attribute.

        Raises:
            BadResponseError: If the status code of the response is between 400 and 600.

        """

        def get_report_msg(content: str) -> str:
            return f'{LINK_KEY}{self.current_url}\n{UA_KEY}{self._user_agent}\n{CONTENT_KEY}{content}'

        # Store response
        response = Response()

        try:
            # Scrape through all URLs in the given list
            for i, crawl_url in enumerate(self.crawl_urls):
                log.debug(f'Scraping page {crawl_url}')
                # Set current page index
                self._current_page = i

                # Fetch the page that we're going to parse
                response = get_response(url=crawl_url, stream=True, user_agent=self._user_agent)

                if self._debug_mode:
                    log.debug(get_report_msg(response.text), console=False, slack=False, store=True)

                if not response.ok:
                    raise BadResponseError(f'<{response.status_code}> Error occurred while connecting to {crawl_url}')

                # Parse the page with LXML, so that we can start doing XPATH queries
                tree: HtmlElement = fromstring(response.content)

                # Scrape the page using DOM
                self._scrape_page(tree)

        except Exception as error:
            from traceback import format_exc

            log.error(format_exc() + get_report_msg(response.text), console=False, slack=False)
            log.error(repr(error), store=False)
