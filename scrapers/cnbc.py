from typing import Optional, List

from scrapers.base_link_scraper import BaseLinkScraper


class CNBCScraper(BaseLinkScraper):

    @property
    def name(self) -> str:
        return 'CNBC'

    @property
    def target_url(self) -> str:
        return 'https://www.cnbc.com'

    @property
    def crawl_urls(self) -> List[str]:
        return [
            'https://www.cnbc.com/business',
            'https://www.cnbc.com/investing'
        ]

    @property
    def element(self) -> Optional[str]:
        return 'Card-titleAndFooter'

    @property
    def sections(self) -> List[str]:
        return ['SectionWrapper-content']
