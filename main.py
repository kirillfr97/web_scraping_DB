from bs4 import BeautifulSoup as BSoup
import pandas as pd
import requests

from scraping.bloomberg import bloomberg
from utils.mongo import update_mongo
from utils.slack import msg_slack


def scrape(url: str, method) -> pd.DataFrame:
    session = requests.Session()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = BSoup(response.text, 'html.parser')

    return method(page)


if __name__ == "__main__":
    bb = scrape('https://www.bloomberg.com/economics', bloomberg)
    message = update_mongo("mongodb+srv://kirill:1234@freecluster.apw2jua.mongodb.net/", bb)
    msg_slack(message)


