import pytest

from web_scraping.scrapers.implicit_scraper import ImplicitLinkScraper
from web_scraping.utils import DataFields


@pytest.mark.parametrize(
    'scraper_info',
    [
        {
            'name': 'QuotesToScrape',
            'target_url': 'https://quotes.toscrape.com',
            'crawl_urls': ['https://quotes.toscrape.com'],
            'filter': '(?:https|/author/)\\S*',
            'sections': [['//*[@class="quote"]/span/a']],
        }
    ],
)
def test_implicit_scraper(connect_db, scraper_info):
    # Create selected scraper
    scraper = ImplicitLinkScraper(**scraper_info)

    # Scrape the web-page
    scraper.start()

    assert not scraper.data.empty

    # Links
    test_links = [
        'https://quotes.toscrape.com/author/Albert-Einstein',
        'https://quotes.toscrape.com/author/J-K-Rowling',
        'https://quotes.toscrape.com/author/Jane-Austen',
        'https://quotes.toscrape.com/author/Marilyn-Monroe',
        'https://quotes.toscrape.com/author/Andre-Gide',
        'https://quotes.toscrape.com/author/Thomas-A-Edison',
        'https://quotes.toscrape.com/author/Eleanor-Roosevelt',
        'https://quotes.toscrape.com/author/Steve-Martin',
    ]

    assert test_links == list(scraper.data[DataFields.Link].values)

    # Update the MongoDB database with the scraped data
    documents = connect_db.update_with_scraper(scraper=scraper)

    assert documents.equals(scraper.data)

    # Delete information from the collection
    connect_db.main_collection.delete_many({DataFields.Name: scraper.name})
