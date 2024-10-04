from requests import ConnectTimeout, Response, get

from web_scraping.log import log


# Default User-Agent
defaultUA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'


def get_response(url: str, stream: bool = False, user_agent: str = defaultUA, timeout: int = 15) -> Response:
    """Sends a GET request to the specified URL with custom headers and returns the response.

    Args:
        url (str): The URL to send the GET request to.
        stream (bool): Whether to enable streaming. Defaults to False.
        user_agent (str): The user agent string to be used for the request. Defaults to 'defaultUA'.
        timeout (int): The timeout value for the request in seconds. Defaults to 15.

    Returns:
        Response: The response object returned by the GET request.

    """
    try:
        # Set up the request headers that are going to be used to simulate a request by the browser
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'User-Agent': user_agent,
        }

        # Send a GET request to the specified URL with a custom headers
        return get(url, stream=stream, timeout=timeout, headers=headers)

    except ConnectTimeout as error:
        from traceback import format_exc

        log.error(format_exc(), console=False, slack=False)
        log.error(repr(error), store=False)
        return Response()
