from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config.helpers import get_slack_token, get_slack_channel


def message_to_slack(message: str):
    # If the message is empty, return without sending a Slack message
    if message == '':
        return

    try:
        # Retrieve the Slack token
        token = get_slack_token()

        # Retrieve the Slack channel
        channel = get_slack_channel()

        # Create a WebClient instance using the Slack token
        client = WebClient(token=token)

        # Send a message to the specified channel
        client.chat_postMessage(channel=channel, text=message)
        print(f'Message was send to Slack Channel \"{channel}\"')

    except SlackApiError as e:
        # Handle any Slack API errors that occur
        print(repr(e))
