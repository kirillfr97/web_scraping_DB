from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.settings import SLACK_CHANNEL
from config.helpers import get_slack_token


def message_to_slack(message: str):
    # If the message is empty, return without sending a Slack message
    if message == '':
        print('Empty message was given')
        return

    # Retrieve the Slack token
    token = get_slack_token()
    if token is None:
        return

    try:
        # Create a WebClient instance using the Slack token
        client = WebClient(token=token)

        # Send a message to the specified channel
        client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

    except SlackApiError as error:
        # Handle any Slack API errors that occur
        print(repr(error))
