from typing import Optional, List

from scrapers.base_link_scraper import BaseLinkScraper


class YahooFinanceScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'YahooFinance'

    @property
    def target_url(self) -> str:
        return 'https://finance.yahoo.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://finance.yahoo.com/news/',
        ]

    @property
    def link_filter(self) -> str:
        return r'(?:https|/news/)\S*'

    @property
    def element(self) -> Optional[str]:
        return 'js-stream-content'

    @property
    def sections(self) -> List[str]:
        return ['tdv2-applet-stream']
