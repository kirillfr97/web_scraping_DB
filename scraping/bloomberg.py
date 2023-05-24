import re
import pandas as pd
from typing import Optional, Tuple
from bs4.element import PageElement
from bs4 import BeautifulSoup as BSoup, Tag

from utils.mongo import MongoData


def get_lnk_title(tag: Tag | PageElement) -> Tuple[Optional[str], Optional[str]]:
    # Extract links and titles from the given tag
    sections = tag.find_all('a', attrs={'href': re.compile(r'https\S*')})
    for section in sections:
        lnk = section.get('href')
        title = section.text
        if lnk != '' and title != '':
            return lnk, title.replace('â€™', '\'')
    return None, None


def get_title_time(tag: Tag | PageElement) -> str:
    # Extract the title time from the given tag
    section = tag.find("div", attrs={"data-component": "recent-timestamp"})
    return section.text if section else ''


def bloomberg(page: BSoup) -> pd.DataFrame:
    # Create an empty DataFrame
    df = pd.DataFrame()

    # Create empty lists to store titles, links, and times
    titles, links, times = [], [], []

    # Specify the sections to extract data from
    sections = [
        "styles_info__E4gXL",  # Main Headline
        "styles_storiesContainer__kLMAY",  # Latest News
    ]

    for section in sections:
        # Find all tags with the specified class in the page
        tags: Tag = page.find(class_=section)
        for tag in tags:
            try:
                # Extract link, title, and title time from the tag
                link, title = get_lnk_title(tag)
                title_time = get_title_time(tag)

                if link not in links and link is not None:
                    # Append unique links, titles, and times to the respective lists
                    links.append(link)
                    titles.append(title)
                    times.append(title_time)

            except Exception as error:
                # Handle any exceptions that occur during extraction
                print(repr(error))

    # Assign the lists as columns in the DataFrame
    df[MongoData.Title] = titles
    df[MongoData.Link] = links
    df[MongoData.Time] = times

    return df
