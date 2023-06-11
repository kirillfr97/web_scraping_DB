from typing import List

from scrapers.base_link_scraper import BaseLinkScraper


class BloombergScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'Bloomberg'

    @property
    def target_url(self) -> str:
        return 'https://www.bloomberg.com'

    @property
    def crawl_urls(self) -> List[str]:
        return ['https://www.bloomberg.com/economics']

    @property
    def link_filter(self) -> str:
        return r'(?:https|/news/)\S*'

    @property
    def sections(self) -> List[str]:
        return [
            'styles_info__E4gXL',  # Main Headline
            'styles_storiesContainer__kLMAY',  # Latest News
        ]
