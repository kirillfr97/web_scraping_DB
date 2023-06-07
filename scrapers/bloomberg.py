from pandas import DataFrame
from re import compile, findall
from typing import Optional, Tuple
from bs4.element import PageElement
from bs4 import BeautifulSoup as BSoup, Tag

from scrapers.base_scraper import BaseScraper
from utils.mongo import MongoData


class BloombergScraper(BaseScraper):

    name = 'Bloomberg'
    crawl_url = 'https://www.bloomberg.com/economics'

    def _scrape_page(self, web_page: BSoup) -> DataFrame:
        # Create an empty DataFrame
        df = DataFrame(columns=[MongoData.Title, MongoData.Link, MongoData.Time])

        # Specify the sections to extract data from
        sections = [
            "styles_info__E4gXL",  # Main Headline
            "styles_storiesContainer__kLMAY",  # Latest News
        ]

        for section in sections:
            # Find all tags with the specified class in the page
            tags: Tag = web_page.find(class_=section)
            for tag in tags:
                try:
                    # Extract link, title, and title time from the tag
                    link, title = self._get_lnk_title(tag)
                    title_time = self._get_title_time(tag)

                    if link is not None and link not in df[MongoData.Link].values:
                        # Append unique link, title, and title_time to DataFrame
                        df.loc[len(df)] = {
                            MongoData.Title: title,
                            MongoData.Link: link,
                            MongoData.Time: title_time
                        }

                except Exception as error:
                    # Handle any exceptions that occur during extraction
                    print(repr(error))

        return df

    @staticmethod
    def _get_lnk_title(tag: Tag | PageElement) -> Tuple[Optional[str], Optional[str]]:
        # Extract links and titles from the given tag
        sections = tag.find_all('a', attrs={'href': compile(r'(?:https|/news/)\S*')})
        for section in sections:
            lnk = section.get('href')
            title = section.text
            if lnk != '' and title != '':
                if len(findall(r'https\S*', lnk)) == 0:
                    lnk = 'https://www.bloomberg.com' + lnk
                return lnk, title.replace('â€™', '\'')
        return None, None

    @staticmethod
    def _get_title_time(tag: Tag | PageElement) -> str:
        # Extract the title time from the given tag
        section = tag.find("div", attrs={"data-component": "recent-timestamp"})
        return section.text if section else ''
