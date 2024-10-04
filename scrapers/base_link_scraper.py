from abc import ABCMeta, abstractmethod
from datetime import datetime
from hashlib import sha1
from re import findall
from typing import List, Optional

from lxml.html import HtmlElement

from web_scraping.scrapers.base_scraper import BaseScraper
from web_scraping.utils import DataFields


class NoDataError(Exception):
    pass


class BaseLinkScraper(BaseScraper, metaclass=ABCMeta):
    @property
    def link_filter(self) -> str:
        """The regular expression pattern to match the link."""
        return r'https\S*'

    @property
    @abstractmethod
    def sections(self) -> List[str]:
        """Specify the sections on pages to extract data from."""
        pass

    @abstractmethod
    def is_sponsored(self, element: HtmlElement) -> bool:
        """Checks whether the article is sponsored or not."""
        pass

    def _get_link_in_tag(self, element: HtmlElement) -> Optional[str]:
        """Extract the link from a given tag.

        This method extracts the link from the given tag based on the regex pattern specified in 'link_filter'.

        Args:
            element (HtmlElement): The HTML object to extract the link from.

        Returns:
            Optional[str]: An extracted link or None if not found.

        """

        link_element = element
        if element.find('a') is not None:
            link_element = element.find('a')
        link = link_element.get('href', '')

        # Checking for empty string
        if link == '':
            return None

        # If it doesn't contain the full URL
        if len(findall(r'https\S*', link)) == 0:
            # Prepend the target_url to the link
            link = self.target_url + link
        return link

    def _scrape_page(self, web_page: HtmlElement):
        # Search through all given XPath
        for path in self.sections[self._current_page]:
            # Extract elements satisfying the XPath
            elements: List[HtmlElement] = web_page.xpath(path)

            if len(elements) == 0:
                raise NoDataError(f'Nothing were found on {path = } on {self.current_url}')

            for element in elements:
                # If element contains sponsored content, then skip it
                if self.is_sponsored(element):
                    continue

                # Extract link from the tag
                link = self._get_link_in_tag(element)

                # Checking for None value
                if link is None:
                    continue

                if link in self._data[DataFields.Link].values:
                    continue

                # Get UTC time
                time = datetime.utcnow()

                # Creating unique hash
                hash_id = sha1((self.name + link).encode()).hexdigest()

                # Append unique link, title and UTC time to DataFrame
                self._data.loc[len(self._data)] = dict(zip(list(DataFields()), [self.name, hash_id, '', link, time, time, '']))
