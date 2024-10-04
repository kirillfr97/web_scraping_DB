import logging
import sys

from datetime import datetime
from re import search, sub
from typing import TextIO

from pymongo.collection import Collection
from slack_sdk import WebClient

from web_scraping.config import (
    ISSUES_COLLECTION,
    ISSUES_DATABASE,
    SLACK_BOT_TOKEN,
    SLACK_CHANNEL,
    SLACK_REPORT_CHANNEL,
    get_env_variable,
)
from web_scraping.utils import IssueFields
from web_scraping.utils.database import MongoDB


def find(pattern: str, text: str) -> str:
    match = search(pattern, text)
    if not match:
        return ''
    return match.group(1)


LINK_KEY = '!LINK'
UA_KEY = '!USERAGENT'
CONTENT_KEY = '!CONTENT'


class LogDBHandler(logging.Handler):
    """Customized logging handler that puts logs to the database."""

    def __init__(self):
        logging.Handler.__init__(self)
        # Specifies the lowest-severity level that determines which messages will be sent
        self.setLevel(logging.DEBUG)

        # Set collection to store logs into
        database_name = get_env_variable(ISSUES_DATABASE)
        collection_name = get_env_variable(ISSUES_COLLECTION)
        self._collection: Collection = MongoDB().get(database_name, collection_name)

    # noinspection PyBroadException
    def emit(self, record: logging.LogRecord):
        if record.getMessage() == '':
            return
        try:
            # Get message
            message = record.getMessage()

            # Find link in the message
            pattern = LINK_KEY + r'\s*([^\s\n]+)'
            link = find(pattern, message)
            message = sub(pattern, "", message).strip()

            # Find user agent in the message
            pattern = UA_KEY + r'\s*([^\n]+)'
            user_agent = find(pattern, message)
            message = sub(pattern, "", message).strip()

            # Find content in the message
            pattern = CONTENT_KEY + r'\s*([\s\S]*)'
            content = find(pattern, message)
            message = sub(pattern, "", message).strip()

            # Insert log into collection
            self._collection.insert_one(
                {
                    IssueFields.Created: datetime.utcnow(),
                    IssueFields.Level: record.levelname,
                    IssueFields.Message: message,
                    IssueFields.Link: link,
                    IssueFields.UserAgent: user_agent,
                    IssueFields.Content: content,
                }
            )

        except Exception:
            self.handleError(record)


class LogSlackHandler(logging.Handler):
    """Customized logging handler that send logs to the Slack channel."""

    def __init__(self):
        logging.Handler.__init__(self)
        # Specifies the lowest-severity level that determines which messages will be sent
        self.setLevel(logging.DEBUG)

        # Retrieve Slack environmental variables
        self._token: str = get_env_variable(SLACK_BOT_TOKEN)
        self._channel: str = get_env_variable(SLACK_CHANNEL)
        self._issue_channel: str = get_env_variable(SLACK_REPORT_CHANNEL)

        # Create a WebClient instance using the Slack token
        self._client = WebClient(token=self._token)

    # noinspection PyBroadException
    def emit(self, record: logging.LogRecord):
        if record.getMessage() == '':
            return
        try:
            # if logging level is DEBUG, then send message to standard Slack channel
            if record.levelno == logging.DEBUG:
                self._client.chat_postMessage(channel=self._channel, text=record.getMessage(), unfurl_links=False, unfurl_media=False)
            # else send formatted message to channel with issues (if level at least INFO)
            elif record.levelno >= logging.INFO:
                self._client.chat_postMessage(channel=self._issue_channel, text=self.format(record), unfurl_links=False, unfurl_media=False)

        except Exception:
            self.handleError(record)


class CustomStreamHandler(logging.StreamHandler):
    """Customized logging handler that send logs into standard stream."""

    def __init__(self, stream: TextIO = sys.stdout):
        super().__init__(stream)

    # noinspection PyBroadException
    def emit(self, record: logging.LogRecord):
        try:
            msg = record.getMessage()
            if record.levelno > logging.DEBUG:
                msg = self.format(record)

            stream = self.stream
            if record.levelno >= logging.ERROR:
                stream = sys.stderr

            stream.write(msg + self.terminator)
            self.flush()

        except RecursionError:
            raise

        except Exception:
            self.handleError(record)
