import pytest

from web_scraping.utils.unfurl import MetaExtractor


metadata_test = [
    {
        'url': 'https://quotes.toscrape.com/',
        'site': 'Quotes to Scrape',
        'title': 'Quotes to Scrape',
        'description': '',
    },
    {
        'url': 'https://www.fnlondon.com/articles/clifford-chance-partner-profit-flat-at-2m-amid-inflationary-pressure-20230719?mod=topic_news',
        'site': '@FinancialNews',
        'title': 'Clifford Chance partner profit flat at £2m amid ‘inflationary pressure’',
        'description': 'Clifford Chance partner profit flatlines after M&A boom tails off',
    },
    {
        'url': 'https://www.bloomberg.com/economics',
        'site': 'Bloomberg.com',
        'title': 'Economics - Bloomberg Facebook Twitter',
        'description': '',
    },
]


class TestMetaExtractor:
    """Class to test the work of MetaExtractor."""

    @pytest.mark.parametrize('data', metadata_test)
    def test_unfurl(self, data):
        # Creating object
        extractor = MetaExtractor()

        # Unfurling
        metadata = extractor.unfurl(url=data.get('url'))

        assert metadata.get('url') == data.get('url'), 'Incorrect url'
        assert metadata.get('site') == data.get('site'), 'Incorrect site'
        assert metadata.get('title') == data.get('title'), 'Incorrect title'
        assert metadata.get('description') == data.get('description'), 'Incorrect description'
