from typing import List, Optional

from scrapers.base_link_scraper import BaseLinkScraper


class ImplicitLinkScraper(BaseLinkScraper):

    def __init__(self, name: str,
                 target_url: str,
                 crawl_urls: List[str],
                 sections: List[str], **kwargs):
        super().__init__()

        self._name = name
        self._target_url = target_url
        self._crawl_urls = crawl_urls
        self._sections = sections

        self._filter: Optional[str] = kwargs.get('filter', None)
        self._element: Optional[str] = kwargs.get('element', None)

    @property
    def name(self) -> str:
        return self._name

    @property
    def target_url(self) -> str:
        return self._target_url

    @property
    def crawl_urls(self) -> List[str]:
        return self._crawl_urls

    @property
    def element(self) -> Optional[str]:
        return self._element

    @property
    def sections(self) -> List[str]:
        return self._sections

    @property
    def link_filter(self) -> str:
        if self._filter is not None:
            return self._filter
        return super().link_filter


if __name__ == '__main__':
    from utils.mongo import MongoData

    # Creating test dictionary
    test = {
        "MarketInsider": {
            "name": "MarketInsider",
            "target_url": "https://markets.businessinsider.com",
            "crawl_urls": [
                "https://markets.businessinsider.com"
            ],
            # "filter": "(?:https|/news/)\\S*",
            "element": "top-story__link",
            "sections": [
                "top-story"
            ]
        }
    }

    for _, test_info in test.items():
        # Creating scraper with information from test file
        scraper = ImplicitLinkScraper(**test_info)

        # Scrape the web-page
        page_data = scraper.start()

        if not page_data.empty:
            print(page_data[MongoData.Title].values)
        else:
            print('Nothing to show!')
