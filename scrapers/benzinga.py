from typing import List

from scrapers.base_link_scraper import BaseLinkScraper


class BenzingaScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'Benzinga'

    @property
    def target_url(self) -> str:
        return 'https://www.benzinga.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://www.benzinga.com/markets',
        ]

    @property
    def sections(self) -> List[str]:
        return [
            'top-section-container',
            'content-feed-list'
        ]
