from typing import Optional, List

from scrapers.base_link_scraper import BaseLinkScraper


class MarketWatchScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'MarketWatch'

    @property
    def target_url(self) -> str:
        return 'https://www.marketwatch.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://www.marketwatch.com/latest-news',
        ]

    @property
    def element(self) -> Optional[str]:
        return 'article__content'

    @property
    def sections(self) -> List[str]:
        return ['component component--layout layout--D2']
