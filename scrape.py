from datetime import datetime
from random import choice
from time import sleep, time
from typing import Dict, List, Union

from web_scraping.config import (
    MAX_FAILED_ATTEMPTS,
    SETTINGS_FILE_NAME,
    TIME_INTERVAL,
    get_env_variable,
)
from web_scraping.log import log
from web_scraping.scrapers.implicit_scraper import ImplicitLinkScraper
from web_scraping.utils.database.wrapper import DBWrapper
from web_scraping.utils.message import create_message, create_summary
from web_scraping.utils.pusher import PusherServer
from web_scraping.utils.response import defaultUA
from web_scraping.utils.settings import get_settings_from_collection


def start():
    # Add arguments
    parser.add_argument('-l', '--loop', help='Necessary argument: run scraping in a loop or not', action='store_true')
    parser.add_argument('-w', '--webpage', help='Unnecessary argument: name of web-page in settings to crawl')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Cycle count
    cycle_count = 0

    # Endless River
    while True:
        cycle_count += 1
        header = f'Cycle #{cycle_count}' if args.loop else 'Single run'
        log.debug(f'--- {header} ---')

        # Run web crawling function
        start_time = time()
        summary = run_crawling()
        total_time = time() - start_time

        # Preparing report
        report = f'```{header} ({datetime.utcnow()}) finished in {total_time:.1f} seconds\n\n{summary}```'

        # Send the summary to Slack
        log.debug(report, console=False, slack=True)

        if not args.loop:
            break

        # Calculate delay
        delay = latency - (time() - start_time)
        if delay > 0:
            log.debug(f'Sleep for {delay:.1f} seconds')
            sleep(delay)


def run_crawling() -> str:
    # Parse the command-line arguments
    args = parser.parse_args()

    # Counter
    counter: Dict[str, List[Union[int, float]]] = {}

    # Getting information about scraped webpages
    scraper_list = get_settings_from_collection(settings_name, 'sources', cluster.settings_collection)
    log.debug(f'Found {len(scraper_list)} websites to scrape')

    # Getting available user agents for crawling
    user_agent_list = get_settings_from_collection(settings_name, 'user_agents', cluster.settings_collection)
    log.debug(f'Found {len(user_agent_list)} user agents for scraping')

    # Iterate over websites described in file
    for scraper_info in scraper_list:
        if args.webpage is not None and args.webpage != scraper_info["name"]:
            continue

        if failed_attempts.get(scraper_info["name"], 0) == number:
            log.error(f'{scraper_info["name"]} was missed due to exceeding the number of failed attempts')
            failed_attempts[scraper_info["name"]] += 1  # This will help to send msg only once
            continue

        # Get random user agent from the list
        user_agent = choice(user_agent_list).get('value', defaultUA)

        # Creating scraper with information from setup file
        scraper = ImplicitLinkScraper(user_agent=user_agent, **scraper_info)

        # Scrape the web-page
        start_time = time()
        scraper.start()
        total_time = time() - start_time

        # if no data were scraped, then increment failed attempts counter for this site, otherwise set it on 0
        failed_attempts[scraper.name] = failed_attempts.get(scraper.name, 0) + 1 if scraper.data.empty else 0

        # Update the MongoDB database with the scraped data and retrieve the message
        documents = cluster.update_with_scraper(scraper=scraper)

        # Send the message to Slack
        log.debug(create_message(documents), console=False, slack=True)

        # Process documents and add them to messages
        pusher.process_table(documents)

        # Add information about webpage {PageName: [num_new_docs, num_parsed_docs]}
        counter.update({scraper.name: [len(documents), len(scraper.data), total_time]})

    # Send messages to Pusher channel
    pusher.notify()

    # Creating summary
    return create_summary(counter)


if __name__ == '__main__':
    # Create an argument parser
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # Init message
    log.info('Server started')

    # Establish connection to pusher channel
    pusher = PusherServer()

    # Establish a connection to the MongoDB cluster
    cluster = DBWrapper()

    # Track failed attempts to scrape webpages (restart app to reset it)
    failed_attempts: Dict[str, int] = {}

    try:
        # Retrieve the latency
        latency = int(get_env_variable(TIME_INTERVAL))

        # Retrieve maximum number of failed attempts
        number = int(get_env_variable(MAX_FAILED_ATTEMPTS))

        # Retrieve settings file name
        settings_name = get_env_variable(SETTINGS_FILE_NAME)

        # Start crawling
        start()

    except Exception as error:
        from traceback import format_exc

        log.critical(format_exc(), slack=False)
        log.critical(repr(error), store=False)

    finally:
        # Close the connection to the MongoDB cluster
        cluster.close()

    log.debug('Finished')
