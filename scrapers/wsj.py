from typing import Optional, List

from scrapers.base_link_scraper import BaseLinkScraper


class WSJScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'WSJ'

    @property
    def target_url(self) -> str:
        return 'https://www.wsj.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://www.wsj.com/news/economy',
        ]

    @property
    def element(self) -> Optional[str]:
        return 'WSJTheme--headline--7VCzo7Ay'

    @property
    def sections(self) -> List[str]:
        return [
            'style--grid--SxS2So51'
        ]
