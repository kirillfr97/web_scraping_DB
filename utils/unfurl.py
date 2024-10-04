from typing import Any, Dict, Optional

from pyquery import PyQuery
from requests import Response

from web_scraping.utils.response import defaultUA, get_response


class MetaExtractor:
    """A class for extracting metadata from web pages.

    Args:
        url (str, optional): The URL of the web page to extract metadata from.
        user_agent (str): The user agent string to be used for the request.
        timeout (int): The timeout value for the HTTP request in seconds.
    """

    def __init__(self, url: Optional[str] = None, user_agent: str = defaultUA, timeout: int = 15):
        """Initialize the MetaExtractor instance."""
        self._data: Dict[str, str] = {}
        self._user_agent: str = user_agent
        self._query: Optional[PyQuery] = None
        self._response: Optional[Response] = None

        if url is not None:
            self._response = get_response(url, user_agent=user_agent, timeout=timeout)
            self._query = PyQuery(self._response.text)

    def is_completed(self) -> bool:
        """Check if the required metadata fields are populated.

        Returns:
            bool: True if the required metadata fields are populated, False otherwise.
        """
        _has_title: bool = self._data.get('title', None) is not None
        _has_description: bool = self._data.get('description', None) is not None
        return _has_title and _has_description

    def unfurl(self, url: Optional[str] = None, user_agent: str = defaultUA, timeout: int = 15) -> Dict[str, str]:
        """Extract metadata from the web page.

        Args:
            url (str, optional): The URL of the web page to extract metadata from.
            user_agent (str): The user agent string to be used for the request.
            timeout (int): The timeout value for the HTTP request in seconds.

        Returns:
            dict: The extracted metadata as a dictionary.

        """
        if url is not None:
            self._response = get_response(url, user_agent=user_agent, timeout=timeout)
            self._query = PyQuery(self._response.text)

        self._data = self._twitter_card()
        if self.is_completed():
            return self._wrap_response('twitter_card')

        self._data.update(self._open_graph())
        if self.is_completed():
            return self._wrap_response('open_graph')

        self._data.update(self._meta_tags())
        return self._wrap_response('meta_tags')

    def _wrap_response(self, method: str) -> Dict[str, str]:
        """Wrap the extracted metadata into a response dictionary.

        Args:
            method (str): The method used to extract the metadata.

        Returns:
            dict: The response dictionary containing the extracted metadata.

        """

        def clear_string(string: str) -> str:
            return string.replace('â€™', '\'').replace('\xa0', ' ').strip()

        def none2str(value: Any) -> str:
            if isinstance(value, str):
                return value
            return ''

        if self._response is None:
            return {}

        css = self._data.get('css', '')
        title = clear_string(none2str(self._data.get('title', '')))
        site = self._data.get('site_name', None)
        description = clear_string(none2str(self._data.get('description', '')))

        return {
            'method': method,
            'url': self._response.url,
            'site': site if site is not None else title,
            'title': title,
            'description': description,
            'css': css,
        }

    def _open_graph(self) -> Dict[str, str]:
        """Extract metadata from Open Graph tags.

        Returns:
            dict: The extracted metadata from Open Graph tags.

        """
        if self._query is None:
            return {}
        return {
            'title': self._query('meta[property=\'og:title\']').attr('content'),
            'site_name': self._query('meta[property=\'og:site_name\']').attr('content'),
            'description': self._query('meta[property=\'og:description\']').attr('content'),
        }

    def _twitter_card(self) -> Dict[str, str]:
        """Extract metadata from Twitter Card tags.

        Returns:
            dict: The extracted metadata from Twitter Card tags.

        """
        if self._query is None:
            return {}
        return {
            'title': self._query('meta[name=\'twitter:title\']').attr('content'),
            'card': self._query('meta[name=\'twitter:card\']').attr('content'),
            'site_name': self._query('meta[name=\'twitter:site\']').attr('content'),
            'creator': self._query('meta[name=\'twitter:creator\']').attr('content'),
            'description': self._query('meta[name=\'twitter:description\']').attr('content'),
        }

    def _meta_tags(self) -> Dict[str, str]:
        """Extract metadata from regular meta tags.

        Returns:
            dict: The extracted metadata from regular meta tags.

        """
        if self._query is None:
            return {}
        return {
            'title': self._query('meta[name=\'title\']').attr('content') or self._query('title').text(),
            'description': self._query('meta[name=\'description\']').attr('content'),
            'image': self._query('meta[name=\'image\']').attr('content'),
            'keywords': self._query('meta[name=\'keywords\']').attr('content'),
        }
