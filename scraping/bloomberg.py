from bs4 import BeautifulSoup as BSoup, Tag
from typing import Optional, Tuple
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import pandas as pd
import requests
import re


SLACK_CHANNEL: str = "test"
SLACK_BOT_TOKEN: str = "xoxb-5310612778596-5305206526405-PJNrT3HOi0okNo9dLWKnyZMO"


def msg_slack(text: str):
    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=text)
    except SlackApiError as error:
        print(repr(error))


def update_mongo(cluster_name: str, data: pd.DataFrame):
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    cluster: MongoClient = MongoClient(cluster_name)

    message: str = ''
    try:
        # Low cost check
        cluster.admin.command('ping')

        database = cluster['News']
        collection = database['Bloomberg']
        collection.delete_many({})
        print(f'Updating...\nAdding {len(data)} new rows')
        for row in data.to_numpy():
            collection.insert_one(dict(zip(data.columns, row)))
            message += f"\"{row[0]}\": {row[1]}\n"

    except ConnectionFailure:
        print('Server not available')
    except Exception as error:
        print(repr(error))
    finally:
        msg_slack(message)
        cluster.close()
    print('Done')


def scrape(url: str, method) -> pd.DataFrame:
    session = requests.Session()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})      
    page = BSoup(response.text, 'html.parser')

    return method(page)


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

    df['title'] = titles
    df['link'] = links
    df['time'] = times
    
    return df


if __name__ == "__main__":
    bb = scrape('https://www.bloomberg.com/economics', bloomberg)
    update_mongo("mongodb+srv://kirill:1234@freecluster.apw2jua.mongodb.net/", bb)
