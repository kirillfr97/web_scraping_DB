from abc import ABCMeta, abstractmethod
from pandas import DataFrame
from re import compile, findall
from typing import Optional, Tuple, List
from bs4 import BeautifulSoup as BSoup, Tag
from bs4.element import PageElement, ResultSet

from utils.mongo import MongoData
from scrapers.base_scraper import BaseScraper


class BaseLinkScraper(BaseScraper, metaclass=ABCMeta):

    @property
    def element(self) -> Optional[str]:
        """Specify the element to search for in sections. """
        return None

    @property
    def link_filter(self) -> str:
        """The regular expression pattern to match the link. """
        return r'https\S*'

    @property
    @abstractmethod
    def sections(self) -> List[str]:
        """Specify the sections on pages to extract data from. """
        pass

    def _get_lnk_title(self, tag: Tag | PageElement) -> Tuple[Optional[str], Optional[str]]:
        """Extract the link and title from a given tag.

        This method extracts the link and title from the given tag based on the regex pattern
        specified in 'link_filter'.

        Args:
            tag (Tag | PageElement): The BeautifulSoup Tag or PageElement object to extract the link and title from.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the extracted link and title,
            or (None, None) if not found.

        """

        def processing(obj: Tag | PageElement) -> Tuple[Optional[str], Optional[str]]:
            # Extract the link and title
            link, text = obj.get('href', ''), obj.text
            # Checking for empty string
            if link == '' or text == '':
                return None, None
            # If it doesn't contain the full URL
            if len(findall(r'https\S*', link)) == 0:
                # Prepend the target_url to the link
                link = self.target_url + link
            return link, text.replace('â€™', '\'').strip()

        # Find all tags within the given tag that match the specified regex pattern
        sections: ResultSet = tag.find_all('a', attrs={'href': compile(self.link_filter)})

        # Iterate over the found tags
        for section in sections:
            lnk, title = processing(section)
            if lnk is None:
                continue
            return lnk, title

        # If nothing found inside tag then trying to extract link from tag itself
        return processing(tag)

    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        # Search through all given sections
        for section in self.sections:
            # Find all tags with the specified class in the page
            tags: Tag = web_page.find(class_=section)

            # If 'element' is set, then find all its instances
            if self.element is not None and tags is not None:
                tags: ResultSet = tags.find_all(class_=self.element)

            if tags is None:
                continue

            for tag in tags:
                try:
                    # Extract link and title from the tag
                    link, title = self._get_lnk_title(tag)

                    if link is not None and link not in self._data[MongoData.Link].values:
                        # Append unique link, title and UTC time to DataFrame
                        self._data.loc[len(self._data)] = {
                            MongoData.Title: title,
                            MongoData.Link: link,
                            MongoData.Time: self._get_article_time()
                        }

                except Exception as error:
                    # Handle any exceptions that occur during extraction
                    print(repr(error))

        return self._data
