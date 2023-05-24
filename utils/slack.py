import os
import json
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"


def get_slack_token(file_path) -> str:
    # This function retrieves the Slack OAuth token from a configuration file
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
        return config['slack']['oauth_token']


def message_to_slack(message: str, channel: str = "test"):
    # If the message is empty, return without sending a Slack message
    if message == '':
        return

    try:
        if SLACK_BOT_TOKEN in os.environ:
            # Retrieve the Slack token from environment variables if available
            token = os.environ.get(SLACK_BOT_TOKEN)
        else:
            # Retrieve the Slack token from a configuration file
            token = get_slack_token('slack_cfg.json')

        # Create a WebClient instance using the Slack token
        client = WebClient(token=token)

        # Send a message to the specified channel
        client.chat_postMessage(channel="#" + channel, text=message)

    except SlackApiError as error:
        # Handle any Slack API errors that occur
        print(repr(error))
