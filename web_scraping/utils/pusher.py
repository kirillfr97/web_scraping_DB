from sys import getsizeof
from typing import Dict, List, Union

from pandas import DataFrame
from pusher import Pusher
from pusher.errors import PusherBadStatus

from web_scraping.config import (
    PUSHER_APP_CLUSTER,
    PUSHER_APP_ID,
    PUSHER_APP_KEY,
    PUSHER_APP_SECRET,
    PUSHER_CHANNEL,
    PUSHER_EVENT,
    get_env_variable,
)
from web_scraping.log import log
from web_scraping.utils import DataFields


# Define necessary constants
MAX_BATCH_SIZE = 10000  # bytes
MAX_TITLE_LENGTH = 300
MAX_DESCRIPTION_LENGTH = 600

# Define type aliases
JSON = Dict[str, str]


def is_fitting(msg: List[JSON]) -> bool:
    """
    Checks if the message fits within the maximum batch size.

    Args:
        msg (List[JSON]): The message to check.

    Returns:
        bool: True if the message fits, False otherwise.

    """
    return getsizeof(str(msg)) <= MAX_BATCH_SIZE


def cut_string_with_ellipsis(text: str, max_size: int) -> str:
    """
    Cuts the given string with ellipsis if its length exceeds the maximum size.

    Args:
        text (str): The text to cut.
        max_size (int): The maximum size of the string.

    Returns:
        str: The cut string.

    """
    if len(text) <= max_size:
        return text

    max_text_size = max_size - len('...')
    return text[:max_text_size] + '...'


class PusherServer:
    """A class that handles communication with Pusher server to notify clients."""

    def __init__(self):
        """Initializes a PusherServer instance."""
        # Messages awaiting to be sent
        self._messages: List[JSON] = []

        # Parameters
        self._event = get_env_variable(PUSHER_EVENT)
        self._channel = get_env_variable(PUSHER_CHANNEL)
        self._pusher_client = Pusher(
            app_id=get_env_variable(PUSHER_APP_ID),
            key=get_env_variable(PUSHER_APP_KEY),
            secret=get_env_variable(PUSHER_APP_SECRET),
            cluster=get_env_variable(PUSHER_APP_CLUSTER),
            ssl=True,
        )

    def process_table(self, data_table: DataFrame):
        """
        Process the data table and store them as pusher messages.

        Args:
            data_table (DataFrame): The data table to process.
        """
        for _, row in data_table.iterrows():
            # Get title and description, cut them if necessary
            title_str = cut_string_with_ellipsis(row[DataFields.Title], MAX_TITLE_LENGTH)
            description_str = cut_string_with_ellipsis(row[DataFields.Description], MAX_DESCRIPTION_LENGTH)

            # Creating pusher message with following data:
            # "n" - "Source Name", "t" - "Article Title", "l" - "Article Link", "d" - "Article Description"
            text = {'n': row[DataFields.Name], 't': title_str, 'l': row[DataFields.Link], 'd': description_str}

            # Add new message
            self._messages.append(text)

    def notify(self):
        """Send messages to Pusher server, which were stored."""
        if len(self._messages) > 0:
            self._split_and_send_messages(self._messages)
            self._messages.clear()

    def trigger(self, message: Union[str, JSON, List[JSON]], channels: Union[List[str], str], event: str):
        """
        Triggers a Pusher event with the given message.

        Args:
            message (Union[str, JSON, List[JSON]]): The message to send.
            channels (Union[List[str], str]): The channels to trigger the event on.
            event (str): The name of the event to trigger.

        """
        if isinstance(message, str):
            message = {'message': message}

        try:
            self._pusher_client.trigger(channels=channels, event_name=event, data=message)

        except PusherBadStatus:
            size = getsizeof(str(message)) / 1024
            log.warning(f'The data content of events must be smaller than 10kB. Content {size = :.2f}kB')

        except Exception as error:
            from traceback import format_exc

            log.error(format_exc(), console=False, slack=False)
            log.error(repr(error), store=False)

    def _split_and_send_messages(self, messages: List[JSON]):
        """
        Send messages to Pusher server, splitting them if necessary.

        Args:
            messages (List[JSON]): The list of messages to send.
        """
        if is_fitting(messages):
            self.trigger(message=messages, channels=self._channel, event=self._event)
        else:
            center = len(messages) // 2 + 1
            self._split_and_send_messages(messages[:center])
            self._split_and_send_messages(messages[center:])
