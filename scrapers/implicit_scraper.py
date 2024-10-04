from typing import List, Optional

from lxml.html import HtmlElement

from web_scraping.scrapers.base_link_scraper import BaseLinkScraper
from web_scraping.utils.response import defaultUA


class ImplicitLinkScraper(BaseLinkScraper):
    def __init__(self, name: str, target_url: str, crawl_urls: List[str], sections: List[str], **kwargs):
        super().__init__()

        self._name = name
        self._target_url = target_url
        self._crawl_urls = crawl_urls
        self._sections = sections

        self._debug_mode: bool = kwargs.get('debug_mode', False)
        self._filter: Optional[str] = kwargs.get('filter', None)
        self._sponsored: Optional[str] = kwargs.get('sponsored', None)
        self._user_agent: Optional[str] = kwargs.get('user_agent', defaultUA)

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
    def sections(self) -> List[str]:
        return self._sections

    @property
    def link_filter(self) -> str:
        if self._filter is not None:
            return self._filter
        return super().link_filter

    def is_sponsored(self, element: HtmlElement) -> bool:
        if self._sponsored is not None:
            if len(element.find_class(self._sponsored)) != 0:
                return True
        return False
