from pandas import DataFrame
from bs4 import BeautifulSoup as BSoup, Tag

from utils.mongo import MongoData
from scrapers.base_scraper import BaseScraper


class BloombergScraper(BaseScraper):

    @property
    def name(self) -> str:
        return 'Bloomberg'

    @property
    def target(self) -> str:
        return 'https://www.bloomberg.com'

    @property
    def crawl_url(self) -> str:
        return 'https://www.bloomberg.com/economics'

    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        # Specify the sections to extract data from
        sections = [
            'styles_info__E4gXL',  # Main Headline
            'styles_storiesContainer__kLMAY',  # Latest News
        ]

        for section in sections:
            # Find all tags with the specified class in the page
            tags: Tag = web_page.find(class_=section)
            for tag in tags:
                try:
                    # Extract link, title, and title time from the tag
                    link, title = self._get_lnk_title(tag, regex=r'(?:https|/news/)\S*')
                    title_time = self._get_title_time(tag, name='div', attrs={'data-component': 'recent-timestamp'})

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
