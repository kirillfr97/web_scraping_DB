from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

SLACK_CHANNEL: str = "test"
SLACK_BOT_TOKEN: str = "xoxb-5310612778596-5305206526405-PJNrT3HOi0okNo9dLWKnyZMO"


def message_to_slack(text: str):
    try:
        # Create a WebClient instance using the SLACK_BOT_TOKEN
        client = WebClient(token=SLACK_BOT_TOKEN)

        # Send a message to the specified SLACK_CHANNEL
        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=text)

    except SlackApiError as error:
        # Handle any Slack API errors that occur
        print(repr(error))
