from pandas import DataFrame
from bs4.element import ResultSet
from bs4 import BeautifulSoup as BSoup

from utils.mongo import MongoData
from scrapers.base_scraper import BaseScraper


class CNBCScraper(BaseScraper):

    @property
    def name(self) -> str:
        return 'CNBC'

    @property
    def target(self) -> str:
        return 'https://www.cnbc.com'

    @property
    def crawl_url(self) -> str:
        return 'https://www.cnbc.com/business'

    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        # Specify the sections to extract data from
        section = 'SectionWrapper-content'

        # Specify the element to search for
        element = 'Card-titleAndFooter'

        # Find all tags with the specified class in the page
        tags: ResultSet = web_page.find(class_=section).find_all(class_=element)
        for tag in tags:
            try:
                # Extract link, title, and title time from the tag
                link, title = self._get_lnk_title(tag, regex=r'https\S*')
                title_time = self._get_title_time(tag, name='span', attrs={'class': 'Card-time'})

                if link is not None and link not in self._data[MongoData.Link].values:
                    # Append unique link, title, and title_time to DataFrame
                    self._data.loc[len(self._data)] = {
                        MongoData.Title: title,
                        MongoData.Link: link,
                        MongoData.Time: title_time
                    }

            except Exception as error:
                # Handle any exceptions that occur during extraction
                print(repr(error))

        return self._data
