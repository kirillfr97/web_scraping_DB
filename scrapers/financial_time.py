from typing import Optional, List

from scrapers.base_link_scraper import BaseLinkScraper


class FinancialTimesScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'FinancialTimes'

    @property
    def target_url(self) -> str:
        return 'https://www.ft.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://www.ft.com/markets',
        ]

    @property
    def link_filter(self) -> str:
        return r'(?:https|/content/)\S*'

    @property
    def element(self) -> Optional[str]:
        return 'o-teaser__heading'

    @property
    def sections(self) -> List[str]:
        return ['css-grid__item-top']
