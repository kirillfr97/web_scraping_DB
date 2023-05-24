from bs4 import BeautifulSoup as BSoup, Tag
from typing import Optional, Tuple
import pandas as pd
import re

from utils.mongo import MongoData


def get_lnk_title(tag: Tag) -> Tuple[Optional[str], Optional[str]]:
    sections = tag.find_all('a', attrs={'href': re.compile(r'https\S*')})
    for section in sections:
        lnk = section.get('href')
        title = section.text
        if lnk != '' and title != '':
            return lnk, title.replace('â€™', '\'')
    return None, None


def get_title_time(tag: Tag) -> str:
    section = tag.find("div", attrs={"data-component": "recent-timestamp"})
    return section.text if section else ''


def bloomberg(page: BSoup) -> pd.DataFrame:
    df = pd.DataFrame()
    titles, links, times = [], [], []
    sections = [
        "styles_info__E4gXL",               # Main Headline
        "styles_storiesContainer__kLMAY",   # Latest News
    ]

    for section in sections:
        tags: Tag = page.find(class_=section)
        for tag in tags:
            try:
                link, title = get_lnk_title(tag)
                title_time = get_title_time(tag)

                if link not in links and link is not None:
                    links.append(link)
                    titles.append(title)
                    times.append(title_time)
                    print(f'News {title=}')

            except Exception as error:
                print(repr(error))

    df[MongoData.Title] = titles
    df[MongoData.Link] = links
    df[MongoData.Time] = times
    
    return df
